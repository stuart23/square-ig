from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

from io import BytesIO
from os import getenv


DRIVE_ID_ENV_VAR = "labels_google_drive_id"
drive_id = getenv(DRIVE_ID_ENV_VAR)
if not drive_id:
    raise Exception('Drive ID Env Var not defined.')

service = build("drive", "v3")


def write_image(content, filename, description, mimetype='image/png', overwrite=False):
    file_metadata = {
        "name": filename,
        "description": description,
        'parents': [drive_id]
    }
    media_body = MediaIoBaseUpload(
        BytesIO(content),
        mimetype=mimetype,
        resumable=True
    )
    if overwrite:
        print(f'Deleting old files with name {filename} before writing.')
        delete_image(filename)
    print(f'Writing {filename} to google drive.')
    file = (
        service.files()
        .create(body=file_metadata, media_body=media_body, supportsAllDrives=True)
        .execute()
    )

def delete_image(filename):
    '''
    Delete all the files with the given filename.
    '''
    files = service.files().list(
        q = f"name = '{filename}'",
        driveId=drive_id,
        corpora='drive',
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
        fields="files(id, name)"
    ).execute().get('files', [])
    print(f'Deleting {len(files)} files.')

    for file in files:
        print(f'Deleting file id f{file}')
        service.files().delete(
            fileId=file['id'],
            supportsAllDrives=True
        ).execute()

if __name__ == '__main__':
    delete_image('0ce96306.png')