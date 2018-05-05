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


def copy_jpg_assets(assets):
    local_files = []
    for asset in assets:
        url = asset.file['url']
        base = url.split('/')[-1]
        # shutil('http:'+url, base)
        local_files.append(base)
    return local_files


def get_jpg_assets(client):
    jpg_assets = []
    return [asset for asset in client.assets() \
        if asset.fields()['file']['contentType'] == 'image/jpeg']


def run_exif_command(command):
    output = subprocess.Popen(command, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, universal_newlines=True)
    message = output.stdout.read()
    output.stdout.close()
    return json.loads(message)


def main():
    delivery_client = ctf.Client(SPACE_ID, ACCESS_TOKEN, environment='master')

    # Find all the jpg/jpeg assets
    jpg_assets = get_jpg_assets(delivery_client)

    # Copy the files from the CMS to a local folder
    local_files = copy_jpg_assets(jpg_assets)

    for asset in jpg_assets:
        # See if there's a linked entry
        linked_entries = delivery_client.entries(
            {'links_to_asset': asset.sys['id']}
        )

        # If there isn't, proceed to the next asset.
        if len(linked_entries) < 1:
            continue

        # Get the subject metadata for each file

        # In each linked entry, see if there's a subject field in the entry
        # for the subject data to go into.
        for entry in linked_entries:
            content_type = entry.sys['content_type'].resolve(delivery_client)
            for field in content_type.fields:
                if field.id != 'subject': continue
                # If so, append each subject term to the linked entry

        # Inject the data into the linked entry

    import code; code.interact(local=locals())


if __name__ == '__main__':
    main()
