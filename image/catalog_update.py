from boto3 import client as Boto3Client
from json import loads
from square_client import get_all_catalog_objects


def handler(event, context):
    objects = get_all_catalog_objects()
    print(objects)

