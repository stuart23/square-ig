from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload


from os import getenv


DRIVE_ID_ENV_VAR = "labels_google_drive_id"

def write_image(content, mimetype='image/png'):
    drive_id = getenv(DRIVE_ID_ENV_VAR)
    if not drive_id:
        raise Exception('Drive ID Env Var not defined.')

    service = build("drive", "v3")
    
    file_metadata = {"name": content.name, 'parents': [drive_id]}
    media_body = MediaIoBaseUpload(
        content,
        mimetype=mimetype,
        resumable=True
    )

    file = (
        service.files()
        .create(body=file_metadata, media_body=media_body, supportsAllDrives=True)
        .execute()
    )