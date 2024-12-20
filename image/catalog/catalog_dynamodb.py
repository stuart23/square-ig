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
    Tries to get an item from the database with a sku. May return more than one
    item as this is not guarenteed to be unique.
    '''
    response = table.query(
        IndexName='skuIndex',
        KeyConditionExpression=Key('SKU').eq(sku)
    )
    if 'Items' not in response.keys():
        raise ValueError('Items not found')
    else:
        items_details = response['Items']
        for item_detail in items_details:
            yield Item(
                sku=item_detail['SKU'],
                price=int(item_detail.get('price')),
                item_id=item_detail.get('item_id'),
                variation_id=item_detail.get('variation_id'),
                pet_safe=item_detail.get('pet_safe'),
                variation_str=item_detail.get('variation_str'),
                item_str=item_detail.get('item_str'),
            )


def get_item_by_variation_id(variation_id):
    '''
    Tries to get an item from the database with an id. Raises ValueError if
    the object does not exist
    '''
    response = table.get_item(Key={"variation_id": variation_id})
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


def upsert_by_id(item):
    """
    Looks for an object and checks that the fields are all the same. If they
    are, it returns false.

    If the record does not exist, or if it is different, it will update the record
    but with the label and website fields set to False so they regenerate.
    """
    try:
        dynamo_item = get_item_by_variation_id(item.variation_id)
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
            Key={'variation_id': item.variation_id},
            UpdateExpression='SET SKU = :SKU, price = :price, item_str = :item_str, variation_str = :variation_str, item_id = :item_id, pet_safe = :pet_safe, label = :label, website = :website',
            ExpressionAttributeValues={
                ':SKU': item.sku,
                ':price': item.price,
                ':item_str': item.item_str,
                ':variation_str': item.variation_str,
                ':item_id': item.item_id,
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
        Key={"variation_id": item.variation_id},
        UpdateExpression='SET website = :website',
        ExpressionAttributeValues={':website': str(datetime.now())}
    )


def set_label_true(item):
    '''
    Sets the label field in the database to the current timestamp for the item.
    '''
    table.update_item(
        Key={"variation_id": item.variation_id},
        UpdateExpression='SET label = :label',
        ExpressionAttributeValues={':label': str(datetime.now())}
    )
    print(f'Marked item {item} as having an image.')


def set_label_false(item):
    '''
    Sets the label field in the database to 'N' for the item.
    '''
    table.update_item(
        Key={"variation_id": item.variation_id},
        UpdateExpression='SET label = :label',
        ExpressionAttributeValues={':label': 'N'}
    )
    print(f'Marked item {item} as not having an image.')


def get_items():
    """
    Returns all the objects in the dynamo database.
    """
    start_key = None
    while True:
        if start_key:
            response = table.scan(ExclusiveStartKey=start_key)
        else:
            response = table.scan()
        for item_details in response.get("Items"):
            yield Item(
                sku=item_details.get('SKU'),
                price=int(item_details.get('price', 0)),
                item_id=item_details.get('item_id'),
                variation_id=item_details.get('variation_id'),
                pet_safe=item_details.get('pet_safe'),
                variation_str=item_details.get('variation_str'),
                item_str=item_details.get('item_str'),
            )

        start_key = response.get("LastEvaluatedKey", None)
        if not start_key:
            break


def delete_item(item):
    '''
    Deletes an individual item from dynamodb.
    '''
    try:
        table.delete_item(Key={"variation_id": item.variation_id})
    except ClientError as err:
        logger.error(
            "Couldn't delete record %s. Here's why: %s: %s",
            sku,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise err