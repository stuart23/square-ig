from boto3 import client as Boto3Client
from json import loads
from os import getenv
from square_client import SquareClient


def handler(event, context):
    body = loads(event['body'])
    try:
        square_event_type = body['type']
        data = body['data']
    except KeyError:
        raise KeyError('Could not parse event: ', event)
    if not data['type'].startswith('customer'):
        raise TypeError('Received non customer data type.')
    id = data['id']
    print(f'Retrieving user {id}')

    instagram_handle = SquareClient().getInstagramHandle(customer_id=id)
    print(f'Instagram Handle is {instagram_handle}')
