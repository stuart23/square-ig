from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload


from os import getenv


DRIVE_ID_ENV_VAR = "labels_google_drive_id"
drive_id = getenv(DRIVE_ID_ENV_VAR)
if not drive_id:
    raise Exception('Drive ID Env Var not defined.')

service = build("drive", "v3")


def write_image(content, mimetype='image/png', overwrite=False):
    file_metadata = {"name": content.name, 'parents': [drive_id]}
    media_body = MediaIoBaseUpload(
        content,
        mimetype=mimetype,
        resumable=True
    )
    if overwrite:
        print(f'Deleting old files with name {content.name} before writing.')
        delete_images(content.name)
    print(f'Writing {content.name} to google drive.')
    file = (
        service.files()
        .create(body=file_metadata, media_body=media_body, supportsAllDrives=True)
        .execute()
    )

def delete_image(filename):
    '''
    Delete all the files with the given filename.
    '''
    fileIds = service.files().list(
        q = f"name = '{filename}'",
        fields="files(id, name)"
    ).execute().get('files', [])
    print(f'Deleting {len(fileIds)} files.')

    for fileId in fileIds:
        print(f'Deleting file id f{fileId}')
        service.files().delete(fileId=fileId).execute()
