from json import loads
from square.client import Client

from auth import TenantClient
from utils import SQSDeserialize, get_secret


def handler(event, context):
    for body in SQSDeserialize(event):
        action = body['action']
        if action == 'new_connection':
            new_connection(**body['data'])
        else:
            raise ValueError(f'No function for action {action}')


def new_connection(**args):
    square_application_credentials = loads(get_secret('square_qr_codes_credentials_arn'))
    square_client = Client()
    print({
            'client_id': square_application_credentials['client_id'],
            'grant_type': 'authorization_code',
            'client_secret': square_application_credentials['client_secret'],
            'code': args['code']
        })
    response = square_client.o_auth.obtain_token(
        body={
            'client_id': square_application_credentials['client_id'],
            'grant_type': 'authorization_code',
            'client_secret': square_application_credentials['client_secret'],
            'code': args['code']
        }
    )
    if not response.is_success():
        raise Exception(f'Token issue request was unsuccessful: {response}')
    print(response)
    print(response.body)
    tenant_client = TenantClient()
    tenant_client.upsert_tenant(oauth_code=args['code'], token_details=response.body)