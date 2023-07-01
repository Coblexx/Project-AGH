from fastapi import APIRouter, HTTPException
from .storage import get_customers_storage, get_orders_storage
from .schema import CustomerCreateSchema, CustomerUpdateSchema, Customer

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sibling_dir = os.path.join(current_dir, '..', 'products')
sys.path.append(sibling_dir)

from products import storage


router = APIRouter()

CUSTOMERS_STORAGE = get_customers_storage()
ORDERS_STORAGE = get_orders_storage()
PRODUCTS_STORAGE = storage.get_products_storage()


@router.post("/add-customer")
async def create_customer(customer: CustomerCreateSchema) -> Customer:
    customer_id = len(CUSTOMERS_STORAGE) + 1
    new_customer = Customer(**customer.dict(), id = customer_id)
    CUSTOMERS_STORAGE[customer_id] = new_customer
    # dodać walidację klientów (pusty klient, cyfry w nazwie, invalid telefon)
    return new_customer


@router.get("/")
async def get_customers() -> list[Customer]:
    return list(get_customers_storage().values())

# ORDER LIST

@router.get("/orders-list")
async def get_orders():
    return ORDERS_STORAGE

# dynamic parameters?????????????? czemu to nie działa | już wiem :D

@router.get("/{customer_id}")
async def get_customer(customer_id: int) -> Customer:
    try:
        return CUSTOMERS_STORAGE[customer_id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Customer with ID={customer_id} does not exist.")
 
@router.get("/orders-list")
async def get_orders():
    return {"message": "1"}


@router.patch("/{customer_id}")
async def update_customer(customer_id: int, updated_customer: CustomerUpdateSchema) -> Customer:
    new_customer = CUSTOMERS_STORAGE[customer_id]
    updated_data = updated_customer.dict(exclude_unset=True)
    for field, value in updated_data.items():
        setattr(new_customer, field, value)
    return new_customer


@router.delete("/{customer_id}")
async def delete_customer(customer_id: int) -> None:
    try:
        del CUSTOMERS_STORAGE[customer_id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Customer with ID={customer_id} does not exist.")


# -------------------
# ORDERS SECTION

@router.post("/{customer_id}/orders")
async def add_customer_order(customer_id: int) -> None:
    order_id = len(ORDERS_STORAGE.get(customer_id, [])) + 1
    new_order = {"id": order_id, "product_list": []}
    ORDERS_STORAGE.setdefault(customer_id, []).append(new_order)
    # dodać walidację klientów
    # dodać order do głownego storage dla orderów (razem z id klienta)
    return ORDERS_STORAGE


@router.patch("/{customer_id}/orders/{order_id}/add-products")
async def add_product_to_order(customer_id:int, order_id: int, product_id: int):
    try:
        order_list = ORDERS_STORAGE[customer_id]
        order = order_list[order_id - 1]

        product = PRODUCTS_STORAGE.get(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        order["product_list"].append(product)
        
        return {"message": "Product added successfully to the order", "product_added": product}
    except KeyError:
        raise HTTPException(status_code=404, detail="Customer or order does not exist")


@router.get("/{customer_id}/orders/{order_id}")
async def get_order_by_id(customer_id: int, order_id: int) -> dict:
    orders_list = ORDERS_STORAGE.get(customer_id)

    for order in orders_list:
        if order["id"] == order_id:
            return order
