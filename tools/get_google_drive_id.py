from os import getenv

from google.oauth2.service_account import Credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


DRIVE_NAME_ENV='drive_name'

def main():
    """
    Gets the google drive id from the drive name in the environment variable `drive_name
    """
    drive_name = getenv(DRIVE_NAME_ENV)

    # credentials = Credentials.from_service_account_file(
    #     "plantsociety-64c848da7bcd.json"
    # )
    # service = build("drive", "v3", credentials=credentials)
    service = build("drive", "v3")

    try:
        results = service.drives().list().execute()
    except HttpError as error:
        raise HttpError(f'Could not retrieve list of drives due to {error}')
    drives = results['drives']
    target_drives = [x for x in drives if x['name'] == drive_name]
    if len(target_drives) != 1:
        raise ValueError(f'Could not find drive or duplicate drive names in {drives}')
    print(f'drive_id=${target_drives[0]}')
    

if __name__ == "__main__":
  main()