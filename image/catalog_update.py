from boto3 import client as Boto3Client
from json import loads


def handler(event, context):
    print('Hello from the catalog Update')
    print(event)