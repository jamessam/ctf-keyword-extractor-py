import contentful as ctf
import contentful_management as mgnt
from flask import Flask, request
import json
import os
import requests
import subprocess
import sys

from PIL import Image, IptcImagePlugin
from PIL.ExifTags import TAGS


ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ENVIRONMENT_ID = 'master'
MGNT_TOKEN = os.environ['MGNT_TOKEN']
SPACE_ID = os.environ['SPACE_ID']


def copy_jpg(asset):
    '''Pulls images from contentful to the server running this app.'''
    url = asset.file['url']
    base = url.split('/')[-1]
    r = requests.get('https:'+url)
    with open(base, 'wb') as local:
        local.write(r.content)


def write_metadata(read_only_entry, keywords):
    '''Writes the IPTC keywords to the contentful-management API. Returns nothing.'''
    entry = mgnt_client.entries(SPACE_ID, ENVIRONMENT_ID).find(
        read_only_entry.id)
    for keyword in keywords:
        try:
            if keyword in entry.fields()['keywords']: continue
        except:
            entry.fields()['keywords'] = []
        entry.fields()['keywords'].append(keyword)
    entry.save()
    entry.publish()


def get_keywords(file_name):
    '''Extracts and returns a list of keywords from the IPTC chunk of a jpg.'''
    keywords = []
    image = Image.open(file_name)
    try:
        keywords_b = IptcImagePlugin.getiptcinfo(image)[(2,25)]
    except KeyError as ke:
        keywords_b = []
    [keywords.append(word.decode('utf-8')) for word in keywords_b]
    return keywords


def keywords_in_content_model(entry):
    '''Examines the content model of a Contentful content entry for a field
    called "keywords", assumed to be a short text list.'''
    content_type = mgnt_client.content_types(
        SPACE_ID,ENVIRONMENT_ID).find(entry.sys['content_type'].id)
    for field in content_type.fields:
        if field.id == 'keywords':
            return True
    return False


def main():
    # See if there's a linked entry. If there isn't, exit.
    linked_entries = delivery_client.entries({'links_to_asset': ASSET_ID})
    if len(linked_entries) < 1:
        sys.exit(f'There are no linked entries for asset {ASSET_ID}.')

    # Get the keyword metadata for each file. If no keyword, exit.
    # Regardless, remove the file.
    for read_only_entry in linked_entries:
        # Look for a keywords field in the linked entry.
        if not keywords_in_content_model(read_only_entry):
            sys.exit(f'There\'s no keywords field in the content model of {read_only_entry}')

        # If so, copy the file from Contentful to the server
        asset = delivery_client.asset(ASSET_ID)
        copy_jpg(asset)

        try:
            keywords = get_keywords(asset.fields()['file']['fileName'])
            write_metadata(read_only_entry, keywords)
        except KeyError as ke:
            print(f'There was a problem writing metadata to the database: {ke}')


app = Flask(__name__)

@app.route("/", methods=('POST',))
def hello():
    global ASSET_ID
    global delivery_client
    global mgnt_client

    if request.method != 'POST':
        return None
    try:
        ASSET_ID = request.form['ASSET_ID']
        delivery_client = ctf.Client(SPACE_ID, ACCESS_TOKEN, environment=ENVIRONMENT_ID)
        mgnt_client = mgnt.Client(MGNT_TOKEN)
    except:
        ASSET_ID = ''

    main()

    return ASSET_ID
