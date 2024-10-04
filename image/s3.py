from boto3 import client as Boto3Client
from os import getenv


s3client = Boto3Client('s3')
BUCKET_NAME = getenv('catalog_bucket_name')


def write_image(image, key):
    print(f"Writing object, {key} to bucket {BUCKET_NAME}")

    # Upload image to s3
    s3client.upload_fileobj(
        image,
        BUCKET_NAME,
        key
    )