'''
Builds a directory of all the labels locally for testing changes.
'''

import sys
from os import environ
from pathlib import Path

pwd = Path(__file__).parent.resolve()
sys.path.append(str(pwd / '..' / 'image'))

environ['square_token_arn'] = 'arn:aws:secretsmanager:us-east-1:015140017687:secret:square_token-oMlH85'
from square_client import get_catalog_items
from labels.label import generate_label

output_dir = pwd / "output"
try:
    output_dir.mkdir()
except FileExistsError:
    pass

items = get_catalog_items()

for item in items:
    label = generate_label(item)
    filename = f'{item.sku_stem}.png'
    print(f'Saving {filename}')
    label.save(output_dir / filename)