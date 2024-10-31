from descriptions import DescriptionsGit
from square_client import get_catalog_items

'''
Recreates all the websites.
'''

if __name__ == "__main__":
    descriptions = DescriptionsGit()
    for item in get_catalog_items():
        descriptions.add_item(item, replace=True)
    descriptions.commit()