from botocore.exceptions import ClientError
from boto3 import resource
from boto3.dynamodb.conditions import Key

table = resource("dynamodb").Table("catalog")


def scan_records():
    """
    Returns all the objects in the dynamo database.
    """
    records = []

    try:
        done = False
        start_key = None
        while not done:
            if start_key:
                response = table.scan(ExclusiveStartKey=start_key)
            else:
                response = table.scan()
            records.extend(response.get("Items", []))
            start_key = response.get("LastEvaluatedKey", None)
            done = start_key is None
    except ClientError as err:
        logger.error(
            "Couldn't scan table. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise err
    return records

def delete_record(record):
    sku = record['SKU']
    try:
        table.delete_item(Key={"SKU": sku})
    except ClientError as err:
        logger.error(
            "Couldn't delete record %s. Here's why: %s: %s",
            sku,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise err


def clear_dynamodb():
    records = scan_records()
    print(f"Deleting {len(records)} records.")
    for record in records:
        delete_record(record)


if __name__ == "__main__":
    clear_dynamodb()