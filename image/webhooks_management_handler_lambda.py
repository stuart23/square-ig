from json import loads

from square.client import Client
from square.http.auth.o_auth_2 import BearerAuthCredentials
from utils import get_secret, getenv_or_raise


def handler(event, context):
    '''
    All messages on the auth SQS topic will trigger this lambda. Depending
    on what is in the message, a different function will be launched.
    Current actions are:
    - configure_webhooks: Will add the webhooks to the catalog endpoint.
    '''
    catalog_update_endpoint = getenv_or_raise('catalog_update_endpoint')
    env_prefix = getenv_or_raise('env_prefix')

    SQUARE_QR_CODES_CREDENTIALS_ARN = "square_qr_codes_token_arn"

    credentials = loads(get_secret(SQUARE_QR_CODES_CREDENTIALS_ARN))
    production_token = credentials["production_token"]
    client = Client(
        bearer_auth_credentials=BearerAuthCredentials(
            access_token=production_token
        ),
        environment='production'
    )

    response = client.webhook_subscriptions.list_webhook_subscriptions()
    assert response.is_success(), f'Request Failed due to: {response.errors}'
    current_subscriptions = response.body.get('subscriptions', [])
    print(f'Current subscriptions: {current_subscriptions}')

    subscription_details = {
        'name': f'{env_prefix} Catalog Update Webhooksss',
        'event_types': [
            'catalog.version.updated'
        ],
        'notification_url': catalog_update_endpoint,
        'api_version': '2021-12-15'
    }

    for test_subscription in current_subscriptions:
        if test_subscription['name'] == subscription_details['name'] \
                and test_subscription['notification_url'] == subscription_details['notification_url']:
            # There is already a subscription with this name and url.
            print('Subscription exists - not adding a new subscription.')
            break
    else:
        print(f'Adding subscription for {catalog_update_endpoint}')
        body = {
            'subscription': subscription_details,
            'idempotency_key': '63f84c6c-2200-4c99-846c-2670a1311fbf'
        }

        result = client.webhook_subscriptions.create_webhook_subscription(body)
        assert result.is_success()
