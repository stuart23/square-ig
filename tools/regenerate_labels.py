from catalog.catalog_dynamodb import set_label_false, get_items


def regenerate_labels():
    records = get_items()
    for record in records:
        set_label_false(record)


if __name__ == "__main__":
    regenerate_labels()