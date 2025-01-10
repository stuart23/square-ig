from decimal import Decimal

from auth import TenantClient, TokenServices
from auth.token_queue import publish
from utils import SQSDeserialize, MetricsHandler


def handler(event, context):
    '''
    All messages on the auth SQS topic will trigger this lambda. Depending
    on what is in the message, a different function will be launched.
    Current actions are:
    - new_connection: Triggered when a new oauth connection is made.
    - find_tokens_to_refresh: Triggered on the aws eventbridge scheduler to
        periodically check what tokens need to be refreshed.
    '''
    for body in SQSDeserialize(event):
        action = body["action"]
        if action == "new_connection":
            data = body['data']
            print(f'Calling new_connection with data: {data}')
            new_connection(**data)
        elif action == "find_tokens_to_refresh":
            print('Calling find_tokens_to_refresh')
            find_tokens_to_refresh()
        elif action == "refresh_token":
            merchant_id = body['data']['merchant_id']
            print(f'Calling refresh token for merchant {merchant_id}')
            refresh_token(merchant_id)
        else:
            raise ValueError(f"No function for action {action}")


def new_connection(**args):
    token_services = TokenServices()
    try:
        token_details = token_services.get_token(code=args["code"])
    except token_services.ExpiredAuthCode:
        print("Token auth code has expired. Skipping this exchange.")
        return
    print(
        "Token successfully retrieved for merchant {merchant_id}".format(
            **token_details
        )
    )
    tenant_client = TenantClient()
    tenant_client.write_token(token_details)


def find_tokens_to_refresh():
    '''
    Reads the database to see if there are any tokens that need to be
    refreshed.
    '''
    tenant_client = TenantClient()
    response = tenant_client.find_tokens_to_refresh()
    if response['Count'] == 0:
        print('No tokens need to be refreshed')
    else:
        print('{} tokens require refresh'.format(response['Count']))
    for item in response['Items']:
        merchant_id = item['merchant_id']
        print(f'Token for {merchant_id} requires refresh.')
        publish(
            {
                "action": "refresh_token",
                "data": {"merchant_id": merchant_id},
            }
        )


def refresh_token(merchant_id):
    '''
    Refreshes the token of a tenant.
    '''
    token_services = TokenServices()
    response = tenant_client.get_merchant(merchant_id, check_single=True)
    merchant_details = response['Items'][0]
    token_details = token_services.get_token(
        refresh_token=merchant_details['refresh_token']
    )
    tenant_client = TenantClient()
