from boto3 import resource
from boto3.dynamodb.conditions import Key
from decimal import Decimal
from datetime import datetime

from .item import Item

table = resource("dynamodb").Table("catalog")


def get_website_needs_update_items():
    '''
    Returns all the items that do not have a website, or it needs updating.
    '''
    response = table.query(
        IndexName='websiteIndex',
        KeyConditionExpression=Key('website').eq('N')
    )
    count = response['Count']
    print(f'{count} objects need their website updated.')
    for item_details in response['Items']:
        yield Item(
            sku=item_details['SKU'],
            price=int(item_details.get('price')),
            item_id=item_details.get('item_id'),
            variation_id=item_details.get('variation_id'),
            pet_safe=item_details.get('pet_safe'),
            variation_str=item_details.get('variation_str'),
            item_str=item_details.get('item_str'),
        )


def get_needs_label_items():
    '''
    Returns all the items that do not have a label, or it needs updating.
    '''
    response = table.query(
        IndexName='labelIndex',
        KeyConditionExpression=Key('label').eq('N')
    )
    count = response['Count']
    print(f'{count} objects need their label updated.')
    for item_details in response['Items']:
        yield Item(
            sku=item_details['SKU'],
            price=int(item_details.get('price')),
            item_id=item_details.get('item_id'),
            variation_id=item_details.get('variation_id'),
            pet_safe=item_details.get('pet_safe'),
            variation_str=item_details.get('variation_str'),
            item_str=item_details.get('item_str'),
        )


def get_item_by_sku(sku):
    '''
    Tries to get an item from the database with a sku. Raises ValueError if
    the object does not exist
    '''
    response = table.query(
        IndexName='skuIndex',
        KeyConditionExpression=Key('SKU').eq(sku)
    )
    if 'Item' not in response.keys():
        raise ValueError('Item not found')
    else:
        item_details = response['Item']
        return Item(
            sku=item_details['SKU'],
            price=int(item_details.get('price')),
            item_id=item_details.get('item_id'),
            variation_id=item_details.get('variation_id'),
            pet_safe=item_details.get('pet_safe'),
            variation_str=item_details.get('variation_str'),
            item_str=item_details.get('item_str'),
        )


def upsert_by_sku(item):
    """
    Looks for an object and checks that the fields are all the same. If they
    are, it returns false.

    If the record does not exist, or if it is different, it will update the record
    but with the label and website fields set to False so they regenerate.
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
                    "variation_id": item.variation_id,
                    "pet_safe": item.pet_safe,
                    "label": 'N',
                    "website": 'N'
                }
            )
        return True
    if dynamo_item == item:
        # Item is the same in Dynamo
        return False
    else:
        # Item is different in Dynamo, updating
        print(f'Item {item} has changed. Updating Dynamo')
        table.update_item(
            Key={'SKU': item.sku},
            UpdateExpression='SET price = :price, item_str = :item_str, variation_str = :variation_str, item_id = :item_id, variation_id = :variation_id, pet_safe = :pet_safe, label = :label, website = :website',
            ExpressionAttributeValues={
                ':price': item.price,
                ':item_str': item.item_str,
                ':variation_str': item.variation_str,
                ':item_id': item.item_id,
                ":variation_id": item.variation_id,
                ':pet_safe': item.pet_safe,
                ':label': 'N',
                ':website': 'N'
            }
        )
        return True


def set_website_true(item):
    '''
    Sets the website field in the database to the current timestamp for the item.
    '''
    table.update_item(
        Key={'SKU': item.sku},
        UpdateExpression='SET website = :website',
        ExpressionAttributeValues={':website': str(datetime.now())}
    )


def set_label_true(item):
    '''
    Sets the label field in the database to the current timestamp for the item.
    '''
    table.update_item(
        Key={'SKU': item.sku},
        UpdateExpression='SET label = :label',
        ExpressionAttributeValues={':label': str(datetime.now())}
    )
    print(f'Marked item {item} as having an image.')