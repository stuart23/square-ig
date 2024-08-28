from boto3 import client as Boto3Client
from json import loads
from square.client import Client as SquareClient


SQUARE_APPLICATION_TOKEN_KEY = 'square_application_token'


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

    square_credentials = getSquareCredentials()
    instagram_handle = getInstagramHandle(
        access_token=square_credentials[SQUARE_APPLICATION_TOKEN_KEY],
        customer_id=id
    )
    print(f'Instagram Handle is {instagram_handle}')

def getInstagramHandle(access_token, customer_id):
    '''
    Takes the Square
    '''
    square_client = SquareClient(access_token=access_token)
    response = square_client.customer_custom_attributes.list_customer_custom_attribute_definitions()
    if response.errors:
        raise ValueError(f'Could not find Instagram Handle Attribute due to: {response.errors}')
    custom_attribute_definitions = response.body['custom_attribute_definitions']

    instagram_handle_attributes = [attribute for attribute in custom_attribute_definitions if attribute['name'] == 'Instagram Handle']
    if len(instagram_handle_attributes) != 1:
        raise ValueError(f'Could not find Instagram Handle in the Customer Custom Attributes list: {custom_attribute_definitions}')
    instagram_handle_key = instagram_handle_attributes[0]['key']

    response = square_client.customer_custom_attributes.retrieve_customer_custom_attribute(
        customer_id=customer_id,
        key=instagram_handle_key
    )
    if response.errors:
        raise ValueError(f'Could not find Instagram Handle for Customer {customer_id}')
    
    return response.body['custom_attribute']['value']

def getSquareCredentials():
    '''
    Gets the credentials `square_application_id` and `square_application_token` from AWS secrets manager.
    '''
    secretsmanager_client = Boto3Client('secretsmanager')
    square_application_id = secretsmanager_client.get_secret_value(SecretId='square_application_id')
    square_application_token = secretsmanager_client.get_secret_value(SecretId=SQUARE_APPLICATION_TOKEN_KEY)
    return {
        'square_application_id': square_application_id, # is this needed?
        SQUARE_APPLICATION_TOKEN_KEY: square_application_token
    }
    