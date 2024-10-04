from qr_leaf import QRLeaf
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
        qr_code = QRLeaf(message['sku'])
        colour_qr = qr_code.colour_qr
        bw_qr = qr_code.bw_qr
        # BytesIO can only be used once, so we make a copy to upload to square
        colour_qr2 = deepcopy(colour_qr)

        write_image(colour_qr, f"{message['sku']}__colour.png")
        write_image(bw_qr, f"{message['sku']}__bw.png")
        create_catalog_image(message, colour_qr2)