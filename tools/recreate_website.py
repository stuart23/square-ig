from descriptions import DescriptionsGit
from square_client import SquareClient

'''
Recreates all the websites.
'''

if __name__ == "__main__":
    descriptions = DescriptionsGit()
    for item in SquareClient().get_catalog_items()
:
        descriptions.add_item(item, replace=True)
    descriptions.commit()