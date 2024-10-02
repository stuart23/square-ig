import io
from boto3 import client as Boto3Client


s3client = Boto3Client('s3')
BUCKET_NAME = getenv('catalog_bucket_name')


def write_image(image, key):
    print(f"Writing object, {key} to bucket {BUCKET_NAME}")
    # Save the image to an in-memory file
    in_mem_file = io.BytesIO()
    image.save(in_mem_file, format=image.format)
    in_mem_file.seek(0)

    # Upload image to s3
    client_s3.upload_fileobj(
        in_mem_file,
        BUCKET_NAME,
        key
    )