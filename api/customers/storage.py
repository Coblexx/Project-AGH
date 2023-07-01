from functools import lru_cache
from .schema import Customer

CustomerStorageType = dict[int, Customer]
CUSTOMERS: CustomerStorageType = {}

@lru_cache()
def get_customers_storage() -> CustomerStorageType:
    return CUSTOMERS
