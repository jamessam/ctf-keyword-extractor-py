import contentful as ctf
import contentful_management as mgnt
import json
import os
import shutil
import subprocess
import sys


SPACE_ID = os.environ['SPACE_ID']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
MGNT_TOKEN = os.environ['MGNT_TOKEN']


def copy_jpg(asset):
    url = asset.file['url']
    base = url.split('/')[-1]
    # shutil.copy('https:'+url, base)


def get_jpg_assets(client):
    jpg_assets = []
    return [asset for asset in client.assets() \
        if asset.fields()['file']['contentType'] == 'image/jpeg']


def run_exif_command(command):
    output = subprocess.Popen(command, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, universal_newlines=True)
    message = output.stdout.read()
    output.stdout.close()
    if 'file not found' in message.lower():
        return None
    return json.loads(message)


def main():
    delivery_client = ctf.Client(SPACE_ID, ACCESS_TOKEN, environment='master')

    # Find all the jpg/jpeg assets
    jpg_assets = get_jpg_assets(delivery_client)

    # Go throught the assets
    for asset in jpg_assets:
        # See if there's a linked entry.
        # If there isn't, proceed to the next asset.
        # TODO: get the entries from the management client
        linked_entries = delivery_client.entries(
            {'links_to_asset': asset.sys['id']}
        )
        if len(linked_entries) < 1:
            continue

        # Copy the file from Contentful to a local folder
        copy_jpg(asset)

        # Get the keyword metadata for each file. If no keyword, move on
        # to the next asset. Regardless, remove the file.
        command = ['exiftool', '-j', asset.file['url'].split('/')[-1]]
        metadata = run_exif_command(command)
        if not metadata:
            print(f'There was a problem with {asset}')
            continue
        # os.remove(asset.file['url'].split('/')[-1])
        try:
            keywords = metadata[0]['Keywords']
        except KeyError as e:
            continue

        # In each linked entry, see if there's a subject field in the entry
        # for the keyword data to go into.
        for entry in linked_entries:
            content_type = entry.sys['content_type'].resolve(delivery_client)
            for field in content_type.fields:
                if field.id != 'keywords':
                    continue
                for keyword in keywords:
                    # Skip words already in there.
                    if keyword in entry.fields()['keywords']:
                        continue
                    entry.fields()['keywords'].append(keyword)
                entry.save()


if __name__ == '__main__':
    main()
