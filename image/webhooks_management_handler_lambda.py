from utils import getenv_or_raise

from square.http.auth.o_auth_2 import BearerAuthCredentials
from json import loads

from square.client import Client
from utils import get_secret


def handler(event, context):
    '''
    All messages on the auth SQS topic will trigger this lambda. Depending
    on what is in the message, a different function will be launched.
    Current actions are:
    - configure_webhooks: Will add the webhooks to the catalog endpoint.
    '''
    api_stage_url = getenv_or_raise('api_stage_url')
    print(api_stage_url)


def configure_webhooks():
    SQUARE_QR_CODES_CREDENTIALS_ARN = "square_qr_codes_token_arn"

    credentials = loads(get_secret(SQUARE_QR_CODES_CREDENTIALS_ARN))
    production_token = credentials["production_token"]
    client = Client(
        bearer_auth_credentials=BearerAuthCredentials(
            access_token=production_token
        ),
        environment='production'
    )
    print(client.webhook_subscriptions.list_webhook_subscriptions())
    body = {
        'subscription': {
            'name': 'Example Webhook Subscription',
            'event_types': [
                'catalog.version.updated'
            ],
            'notification_url': 'https://example-webhook-url.com',
            'api_version': '2021-12-15'
        },
        'idempotency_key': '63f84c6c-2200-4c99-846c-2670a1311fbf'
    }

    result = client.webhook_subscriptions.create_webhook_subscription(body)


if __name__ == '__main__':
    configure_webhooks('MLXNPCP2AHNKX')