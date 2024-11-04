import google.auth
from google.auth.identity_pool import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def handler(event, context):
    credentials, project_id = google.auth.default()
    service = build("drive", "v3")

    try:
        results = service.drives().list().execute()
    except HttpError as error:
        print('Could not retrieve list of drives.')
        raise error
    drives = results['drives']
    target_drives = [x for x in drives if x['name'] == drive_name]
    if len(target_drives) != 1:
        raise ValueError(f'Could not find drive \"{drive_name}\" or duplicate drive names in {drives}')
    print(f'drive_id={target_drives[0]["id"]}')
    