'''
Gets all the items from square and then tries each sku/hyperlink to see if it is working.
'''

from os import environ
from requests import request

environ['square_token_arn'] = 'arn:aws:secretsmanager:us-east-1:015140017687:secret:square_token-oMlH85'
from square_client import get_catalog_items

def main():
    items = get_catalog_items()
    for item in items:
        response = request(url='https://' + item.sku, method='GET')
        if response.ok:
            print('{} [ \033[92mOK \033[0m]'.format(item.sku))
        else:
            print('{} [ \033[91mERROR \033[0m]'.format(item.sku))

if __name__ == '__main__': main()