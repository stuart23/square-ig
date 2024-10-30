from boto3 import resource
from boto3.dynamodb.conditions import Key
from decimal import Decimal

from .item import Item

table = resource("dynamodb").Table("catalog")


def get_item(sku):
    '''
    Tries to get an item from the database with a sku. Raises ValueError if
    the object does not exist
    '''
    response = table.get_item(Key={"SKU": sku})
    if 'Item' not in response.keys():
        raise ValueError('Item not found')
    else:
        item_details = response['Item']
        return Item(
            sku=item_details['SKU'],
            price=int(item_details['price']),
            item_id=item_details['item_id'],
            pet_safe=item_details['pet_safe'],
            variation_str=item_details['variation_str'],
            item_str=item_details['item_str'],
        )


def upsert_by_sku(item):
    """
    Looks for an object and checks that the fields are all the same. If they
    are, it returns false.

    If the record does not exist, or if it is different, it will update the record
    but with the barcode and website fields set to False so they regenerate.
    """
    try:
        dynamo_item = get_item(item.sku)
    except ValueError:
        # No item with this sku exists, adding it.
        print(f'Adding item to DynamoDB: {item.item_str} - {item.variation_str}')
        table.put_item(
                Item={
                    "SKU": item.sku,
                    "price": item.price,
                    "item_str": item.item_str,
                    "variation_str": item.variation_str,
                    "item_id": item.item_id,
                    "pet_safe": item.pet_safe,
                    "barcode": False,
                    "website": False
                }
            )
        return True
    if dynamo_item == item:
        # Item is the same in Dynamo
        return False
    else:
        # Item is different in Dynamo, updating
        print('Item has changed. Updating Dynamo')
        table.update_item(
            Key={'SKU': item.sku},
            UpdateExpression='SET price = :price, item_str = :item_str, variation_str = :variation_str, item_id = :item_id, pet_safe = :pet_safe, barcode = :barcode, website = :website',
            ExpressionAttributeValues={
                ':price': item.price,
                ':item_str': item.item_str,
                ':variation_str': item.variation_str,
                ':item_id': item.item_id,
                ':pet_safe': item.pet_safe,
                ':barcode': False,
                ':website': False
            }
        )
        return True

if __name__ == '__main__':
    upsert_by_sku(
        Item(
            sku='plantsoc.com/ATL-N-261zzz',
            price=1234,
            item_str='test234',
            variation_str='test description',
            item_id='abcd',
            pet_safe=False
        )
    )