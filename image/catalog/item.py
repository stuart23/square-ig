from dataclasses import dataclass

from uuid import uuid4


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
            self.sku = '/'.join([URL_PREFIX, str(uuid4()).replace('-', '')[:8]])
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