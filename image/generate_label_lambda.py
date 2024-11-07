from labels import generate_label_bytes
from s3 import write_image
from json import loads
from copy import deepcopy

from catalog import Item
from catalog.catalog_dynamodb import set_label_true
from gdrive import write_image

def handler(event, context):
    # Should be only one record, but lets loop just in case.
    for record in event['Records']:
        print(f'Processing record: {record}')
        try:
            message = record['Sns']['Message']
        except KeyError:
            print(f'Could not find a message in {record}')
        message = loads(message)
        item = Item(**message)
        filename = f'{item.sku_stem}.png'
        label = generate_label_bytes(item, filename=filename)
        # BytesIO can only be used once, so we make a copy to upload to square
        label2 = deepcopy(label)

        write_image(label, filename)
        # Unset to update item
        write_image(item, label2)
        set_label_true(item)