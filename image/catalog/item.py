from dataclasses import dataclass
from typing import Optional
from re import match

URL_PREFIX = "plantsoc.com"
SKU_FORMAT = '^[A-Za-z0-9-]{3,9}$' # 3 to 8 alphanumeric characters

@dataclass
class Item:
    '''
    A square item.
    '''
    sku: str
    price: int
    item_str: str
    variation_str: str
    item_id: str
    variation_id: str
    pet_safe: bool
    categories: Optional[list] = None

    @classmethod
    def fromSquareDetails(cls, item_str, variation_details, custom_attribute_values={}, categories=None):
        '''
        Creates a new item from the item string and variation details.

        The item is created from variation_details, but the item name
        is not included in the variation_details so it must be passed
        in separately.
        '''
        # Try and get the pet_safe status from the custom_attribute_values
        item_details = {'item_str': item_str, 'pet_safe': False}
        if custom_attribute_values:
            for custom_attribute in custom_attribute_values.values():
                if custom_attribute.get('name', '') == 'Pet Safe':
                    item_details['pet_safe'] = custom_attribute['boolean_value']
                    break
        item_variation_data = variation_details['item_variation_data']
        item_details['sku'] = item_variation_data.get('sku')
        item_details['variation_str'] = item_variation_data['name']
        item_details['item_id'] = item_variation_data["item_id"]
        item_details['variation_id'] = variation_details['id']
        try:
            item_details['price'] = item_variation_data['price_money']['amount']
        except KeyError:
            item_details['price'] = 0
        item_details['categories'] = categories
        return cls(**item_details)

    def __eq__(self, other):
        '''
        Check equality
        '''
        if not self.sku == other.sku:
            return False
        elif not self.price == other.price:
            return False
        elif not self.item_str == other.item_str:
            return False
        elif not self.variation_str == other.variation_str:
            return False
        elif not self.item_id == other.item_id:
            return False
        elif not self.variation_id == other.variation_id:
            return False
        elif not self.pet_safe == other.pet_safe:
            return False
        else:
            return True


    def is_category(self, category):
        '''
        Returns true if the items categories contain the given 'category'.

        Categories are just expressed as their names, e.g. item.is_category('Plants')
        '''
        if self.categories == None:
            return False
        if any([x['name'] == category for x in self.categories]):
            return True
        else:
            return False


    def update_sku(self):
        """
        Rewrites the sku with the format URL_PREFIX/sku.

        If there is no sku, one will be generated and True will be returned

        If it does not begin with the URL_PREFIX, it will be rewritten in the variation dict
        with a sku beginning with the URL_PREFIX.

        If the item has the name `no_sku*`, then it will not be changed.
        """
        # No sku
        if not self.sku:
            self.sku = '/'.join([URL_PREFIX, self.variation_id[:8]])
            return True
        if self.sku.startswith(URL_PREFIX):
            return False
        elif self.item_str.startswith('no_sku'):
            return False
        else:
            new_sku = '/'.join([URL_PREFIX, self.sku])
            print(f"SKU {self.sku} does not start with {URL_PREFIX}. Updating to {new_sku}")
            self.sku = new_sku
            return True

    def validate_sku(self):
        '''
        First checks that the sku is alphanumeric characters only. If not, we use the first 8 chars of the variation ID.

        Checks that the sku doesn't already exist in the database. If the sku exists, we use the first 8 chars of the variation ID.

        If the sku exists but already belongs to this item, then it is unchanged.
        '''
        from .catalog_dynamodb import get_item_by_sku

        is_valid = True

        # If the sku is not alphanumeric, then we replace it with the first 8 chars of the variation_id.
        if not match(SKU_FORMAT, self.sku_stem):
            new_sku = '/'.join([URL_PREFIX, self.variation_id[:8]])
            print(f'Item with sku {self.sku} is not valid. Changing the sku to {new_sku}')
            self.sku = new_sku
            is_valid = False

        db_items = list(get_item_by_sku(self.sku))

        # If there is another entry in the database that has a different variation id, then we replace
        # this items sku with the first 8 chars of the variation_id.
        if any([db_item.variation_id != self.variation_id for db_item in db_items]):
            new_sku = '/'.join([URL_PREFIX, self.variation_id[:8]])
            print(f'Item with sku {self.sku} already exists in the database. Changing the sku to {new_sku}')
            self.sku = new_sku
            is_valid = False

        return is_valid


    @property
    def sku_stem(self):
        """
        Returns just the last bit of the sku - the path. E.g. if the sku is `plantsoc.com/abcd1234`, returns just `abcd1234`
        """
        if self.sku is not None:
            return self.sku.replace(f"{URL_PREFIX}/", "")
        else:
            return None

    @property
    def square_link(self):
        '''
        Returns a link to square to the exact item.
        '''
        item_id = self.item_id
        return f'https://app.squareup.com/dashboard/items/library/{item_id}'