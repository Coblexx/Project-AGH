from functools import lru_cache

from .schema import Order

OrderStorageType = dict[int, Order]
ORDERS: OrderStorageType = {}


@lru_cache()
def get_customers_storage() -> OrderStorageType:
    return ORDERS
