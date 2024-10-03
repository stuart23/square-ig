from boto3 import client as Boto3Client
from json import loads
from os import getenv
from square_client import getInstagramHandle
from ensta import Web


SQUARE_ACCESS_TOKEN_KEY = 'square_access_token'


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

    instagram_handle = getInstagramHandle(customer_id=id)
    print(f'Instagram Handle is {instagram_handle}')

    instagram_credentials = getInstagramCredentials()
    enstaClient = Web(**instagram_credentials)
    profile = enstaClient.profile("leomessi")
    print(profile.full_name)
    print(profile.biography)


def getInstagramCredentials():
    '''
    Gets the credentials `square_application_id` and `square_application_token` from AWS secrets manager.
    '''
    credentials_arn = getenv('instagram_credentials_arn')
    secretsmanager_client = Boto3Client('secretsmanager')
    instagram_credentials = secretsmanager_client.get_secret_value(SecretId='credentials_arn')['SecretString']
    username = instagram_credentials['username']
    print(f'Retrieved credentials for user {username}')
    return instagram_credentials