from labels import generate_label
from s3 import write_image
from json import loads
from copy import deepcopy

from square_client import create_catalog_image


def handler(event, context):
    # Should be only one record, but lets loop just in case.
    for record in event['Records']:
        print(f'Processing record: {record}')
        try:
            message = record['Sns']['Message']
        except KeyError:
            print(f'Could not find a message in {record}')
        message = loads(message)
        print(message)
        label = generate_label_bytes(
            sku=message['sku'],
            title=message['title'],
            variation=message['variation'],
            price=message['price'],
            pet_safe=message['pet_safe']
        )
        # BytesIO can only be used once, so we make a copy to upload to square
        label2 = deepcopy(label)

        write_image(label, f"{message['sku']}.png")
        create_catalog_image(message, label2)