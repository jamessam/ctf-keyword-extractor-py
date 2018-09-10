import contentful as ctf
import contentful_management as mgnt
import os
import requests
import sys

from PIL import Image, IptcImagePlugin
from PIL.ExifTags import TAGS


# CONSTANTS
cda = ctf.Client(
    os.environ['SPACE_ID'],
    os.environ['ACCESS_TOKEN'],
    environment='master')
cma = mgnt.Client(os.environ['MGNT'])


# FUNCTIONS
def check_for_keywords(entry):
    '''Examines the content model of a Contentful content entry for a field
    called "keywords", assumed to be a short text list.'''
    content_type = cma.content_types(os.environ['SPACE_ID'],'master').find(
        entry.sys['content_type'].id)
    for field in content_type.fields:
        if field.id == 'keywords':
            return True
    return False


def copy_jpg(asset):
    '''Pulls images from contentful to the server running this app.'''
    url = asset.file['url']
    base = url.split('/')[-1]
    r = requests.get('https:'+url)
    with open(f'/tmp/{base}', 'wb') as local:
        local.write(r.content)


def get_keywords(file_name):
    '''Extracts and returns a list of keywords from the IPTC chunk of a jpg.'''
    keywords = []
    image = Image.open(file_name)
    try:
        keywords_b = IptcImagePlugin.getiptcinfo(image)[(2,25)]
    except KeyError as ke:
        keywords_b = []
    [keywords.append(word.decode('utf-8')) for word in keywords_b]
    os.remove(file_name)
    return keywords


def write_metadata(read_only_entry, keywords):
    '''Writes the IPTC keywords to the contentful-management API. Returns nothing.'''
    entry = cma.entries(os.environ['SPACE_ID'], 'master').find(
        read_only_entry.id)
    for keyword in keywords:
        try:
            if keyword in entry.fields()['keywords']: continue
        except:
            entry.fields()['keywords'] = []
        entry.fields()['keywords'].append(keyword)
    entry.save()
    entry.publish()


def main(assetId):
    print(f'Starting extractor for {assetId}')
    # See if there's a linked entry. If there isn't, exit.
    linked_entries = cda.entries({'links_to_asset': assetId})
    if len(linked_entries.items) < 1:
        sys.exit(f'There are no linked entries for asset {assetId}.')

    # Filter out the entries with no keywords field on its content type.
    filtered_entries = [entry for entry in linked_entries if check_for_keywords(entry)]
    if len(filtered_entries) == 0:
        sys.exit(f'There are no entries with a keywords field attached to {assetId}')

    # Load the asset object
    asset = cda.asset(assetId)

    # Copy the file from Contentful to the server
    copy_jpg(asset)

    # Extract the keywords and write them to the appropriate records
    try:
        file_name = f"/tmp/{asset.fields()['file']['fileName']}"
        keywords = get_keywords(file_name)
        [write_metadata(entry, keywords) for entry in filtered_entries]
    except KeyError as ke:
        print(f'There was a problem writing metadata to the database: {ke}')

    return None


if __name__ == '__main__':
    main(sys.argv[1])
