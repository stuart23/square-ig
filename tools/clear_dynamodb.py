from catalog.catalog_dynamodb import delete_item, get_items


def clear_dynamodb():
    records = get_items()
    for record in records:
        print(f'Deleting {record}')
        delete_item(record)


if __name__ == "__main__":
    clear_dynamodb()