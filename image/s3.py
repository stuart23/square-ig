from boto3 import client
from os import getenv


s3client = client('s3')
BUCKET_NAME = getenv('catalog_bucket_name')
if not BUCKET_NAME:
    raise Exception('Env var catalog_bucket_name not set.')


def write_image(image, filename):
    print(f"Writing object, {filename} to bucket {BUCKET_NAME}")

    # Upload image to s3
    s3client.put_object(
        Body=image,
        Bucket=BUCKET_NAME,
        Key=filename
    )