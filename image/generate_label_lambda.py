from json import loads
from copy import deepcopy
from json import dumps

from labels import generate_label
from s3 import write_image as s3_write_image
from catalog import Item
from catalog.catalog_dynamodb import set_label_true
from gdrive import write_image as gdrive_write_image

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
        label = generate_label(item)

        s3_write_image(label, filename)

        description = dumps(item.__dict__)
        gdrive_write_image(label, filename, description, overwrite=True)
        set_label_true(item)

if __name__ == '__main__':
    item = Item(
        sku='plantsoc.com/abcd1234',
        price=123,
        item_str='abc',
        variation_str='abc',
        item_id='qwerty',
        variation_id='asdfg',
        pet_safe=True
    )
    from json import dumps
    handler({'Records':[{'Sns': {'Message': dumps(item.__dict__)}}]}, None)