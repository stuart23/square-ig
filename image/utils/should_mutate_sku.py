from utils import getenv_or_raise


def should_mutate_sku(merchant_details):
    '''
    Takes the merchant details dict from `tenant_client.get_merchant`
    and works out if the skus should be mutated.
    '''
    try:
        env = getenv_or_raise('env')
    except KeyError:
        print('`env` variable is not set in environment. '
              'skus will not be mutated.')
        return False

    key = f'{env}_update_skus'
    merchant_id = merchant_details['id']
    try:
        update_skus = merchant_details[key]
    except KeyError:
        print(f'Merchant {merchant_id} did not have key {key}')
        return False
    status = f'Merchant {merchant_id} has {key} set to {update_skus}.'
    if update_skus:
        print(f'{status} Skus will be mutated')
        return True
    else:
        print(f'{status} Skus will not be mutated')
        return False
