from functools import lru_cache

from .schema import Product

ProductStorageType = dict[int, Product]
PRODUCTS: ProductStorageType= {}

@lru_cache()
def get_products_storage() -> ProductStorageType:
    return PRODUCTS
