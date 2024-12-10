'''
Gets all the items from square and then tries each sku/hyperlink to see if it is working.
'''

from os import environ
from requests import request

environ['square_token_arn'] = 'arn:aws:secretsmanager:us-east-1:015140017687:secret:square_token-oMlH85'
from square_client import SquareClient

def main():
    items = SquareClient().get_catalog_items()
    failed_websites = []
    total_item_count = 0
    for item in items:
        if item.item_str == 'no_sku':
            continue
        response = request(url='https://' + item.sku, method='GET')
        total_item_count += 1
        if response.ok:
            print('{} [ \033[92mOK \033[0m]'.format(item.sku))
        else:
            print('{} [ \033[91mERROR \033[0m]'.format(item.sku))
            failed_websites.append(item)

    print()
    print(f'{len(failed_websites)} / {total_item_count} failed')
    if len(failed_websites) > 0:
        exit(1)

if __name__ == '__main__': main()