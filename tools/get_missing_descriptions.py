'''
Looks at all the items that belong to the plants category and checks their website to make sure it is
not default. Any default templated pages will contain 'This is an item.'.
'''

from os import environ
from requests import request

environ['square_token_arn'] = 'arn:aws:secretsmanager:us-east-1:015140017687:secret:square_token-oMlH85'
from square_client import SquareClient
from descriptions import DescriptionsGit

def main():
    items = SquareClient().get_catalog_items()
    descriptions = DescriptionsGit()
    base_dir = descriptions.repo_dir / "content"
    for item in items:
        if item.is_category('Plants'):
            item_dir = base_dir / item.sku_stem
            readme = item_dir / 'index.md'
            if not item_dir.is_dir():
                raise Exception(f'Directory {item_dir} does not exist.')
            if not readme.exists():
                raise Exception(f'Readme {readme} does not exist.')
            with open(readme) as fh:
                contents = fh.readlines()
            gh_url = f'https://github.com/stuart23/plantsoc.com/tree/main/content/{item.sku_stem}/index.md'
            if 'This is an item.' in contents:
                print(f'{item.sku} [ \033[91mMISSING \033[0m] {gh_url}')
            else:
                print(f'{item.sku} [ \033[92mOK \033[0m] {gh_url}')


if __name__ == '__main__': main()