from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


from os import getenv


DRIVE_ID_ENV_VAR = "labels_google_drive_id"

def writeFile():
    drive_id = getenv(DRIVE_ID_ENV_VAR)
    if not drive_id:
        raise Exception('Drive ID Env Var not defined.')

    service = build("drive", "v3")
    
    file_metadata = {"name": "pet_safe.png", 'parents': [drive_id]}
    media = MediaFileUpload("labels/assets/pet_safe.png", mimetype="image/png")

    file = (
        service.files()
        .create(body=file_metadata, media_body=media, supportsAllDrives=True)
        .execute()
    )