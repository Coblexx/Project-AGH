from functools import lru_cache
from .schema import Customer
from typing import Dict, List

OrderStorageType = Dict[int, List[Dict[str, int]]]
ORDERS_STORAGE: OrderStorageType = {}

CustomerStorageType = dict[int, Customer]
CUSTOMERS: CustomerStorageType = {}

@lru_cache()
def get_customers_storage() -> CustomerStorageType:
    return CUSTOMERS


@lru_cache()
def get_orders_storage() -> OrderStorageType:
    return ORDERS_STORAGE
