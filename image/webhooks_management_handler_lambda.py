from square_client import SquareClient
from utils import getenv_or_raise


def handler(event, context):
    '''
    All messages on the auth SQS topic will trigger this lambda. Depending
    on what is in the message, a different function will be launched.
    Current actions are:
    - configure_webhooks: Will add the webhooks to the catalog endpoint.
    '''
    catalog_update_endpoint = getenv_or_raise('catalog_update_endpoint')
    env_prefix = getenv_or_raise('env_prefix')

    client = SquareClient()

    current_subscriptions = client.get_webhooks()
    print(f'Current subscriptions: {current_subscriptions}')

    subscription_details = {
        'name': f'{env_prefix} Catalog Update Webhook',
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
        client.add_webhook(subscription_details)