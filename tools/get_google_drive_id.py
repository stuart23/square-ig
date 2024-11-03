from os import getenv
from json import load
from google.auth.identity_pool import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


DRIVE_NAME_ENV='drive_name'

def main():
    """
    Gets the google drive id from the drive name in the environment variable `drive_name
    """
    drive_name = getenv(DRIVE_NAME_ENV)
    credentials_file = getenv["GOOGLE_APPLICATION_CREDENTIALS"]
    if not credentials_file:
        raise Exception('Environment Variable GOOGLE_APPLICATION_CREDENTIALS is not set.')
    with open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]) as f:
        key = load(f)
    credentials = Credentials.from_info(key)
    service = build("drive", "v3")

    try:
        results = service.drives().list().execute()
    except HttpError as error:
        print('Could not retrieve list of drives.')
        raise error
    drives = results['drives']
    target_drives = [x for x in drives if x['name'] == drive_name]
    if len(target_drives) != 1:
        raise ValueError(f'Could not find drive or duplicate drive names in {drives}')
    print(f'drive_id=${target_drives[0]}')
    

if __name__ == "__main__":
  main()