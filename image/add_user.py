from boto3 import client as Boto3Client
from json import loads
from os import getenv
from square_client import getInstagramHandle
from ensta import Web


INSTAGRAM_CREDENTIALS_ARN_ENV = 'instagram_credentials_arn'


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
    Gets the instagram username and password from AWS secrets manager.
    '''
    credentials_arn = getenv(INSTAGRAM_CREDENTIALS_ARN_ENV)
    secretsmanager_client = Boto3Client('secretsmanager')
    instagram_credentials = secretsmanager_client.get_secret_value(SecretId=credentials_arn)['SecretString']
    username = instagram_credentials['username']
    print(f'Retrieved credentials for user {username}')
    return instagram_credentials