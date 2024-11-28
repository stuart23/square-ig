from square.http.auth.o_auth_2 import BearerAuthCredentials
from square_client import SquareClient
from boto3 import client as Boto3Client


def batch_filter_images(object_ids):
    to_delete = []
    response = catalog.batch_retrieve_catalog_objects(
        body={
            "object_ids":object_ids,
            "include_related_objects":False,
            "catalog_version":None,
            "include_category_path_to_root":False
        }
    )
    try:
        objects = response.body['objects']
    except KeyError:
        print(f'No images retrieved because {response}')
        return
    for image in objects:
        if image['image_data'].get('caption') == 'QR Code':
            to_delete.append(image['id'])
    print(f'Deleting {len(to_delete)} images')
    catalog.batch_delete_catalog_objects(body={"object_ids":to_delete})


if __name__ == '__main__':
    items = get_all_catalog_items()
    catalog = get_square_client().catalog

    for item in items:
        print(item['item_data']['name'])
        images = item['item_data'].get('image_ids', [])
        print(f'Number of images: {len(images)}')
        object_ids = []
        to_delete = []
        for image_id in images:
            object_ids.append(image_id)
            if len(object_ids) >= 100:
                batch_filter_images(object_ids)
                object_ids = []
                to_delete = []
        else:
            batch_filter_images(object_ids)


            # image = catalog.retrieve_catalog_object(
            #     object_id=image_id,
            #     include_related_objects=False,
            #     catalog_version=None,
            #     include_category_path_to_root=False
            # )