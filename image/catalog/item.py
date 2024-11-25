from dataclasses import dataclass
from typing import Optional

URL_PREFIX = "plantsoc.com"


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
        Checks that the sku doesn't already exist in the database.
        
        If the sku exists, a new one will be generated for the item.

        If the sku exists but already belongs to this item, then it is unchanged.
        '''
        from .catalog_dynamodb import get_item_by_sku
        is_valid = True
        while True:
            db_items = list(get_item_by_sku(self.sku))

            # If there is another entry in the database that has a different variation id, then we replace this.
            if any([db_item.variation_id != self.variation_id for db_item in db_items]):
                is_valid = False
                new_sku = '/'.join([URL_PREFIX, self.variation_id[:8]])
                print(f'Item with sku {self.sku} already exists in the database. Changing the sku to {new_sku}')
                self.sku = new_sku
            else:
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