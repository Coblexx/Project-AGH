from fastapi import APIRouter, HTTPException
from .storage import get_customers_storage, get_orders_storage
from .schema import CustomerCreateSchema, CustomerUpdateSchema, Customer

import os, sys 

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
    return new_customer


@router.get("/")
async def get_customers() -> list[Customer]:
    return list(CUSTOMERS_STORAGE.values())

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
async def create_order(customer_id: int):
    if customer_id not in CUSTOMERS_STORAGE:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    order_id = len(ORDERS_STORAGE) + 1
    customer_name = f"{CUSTOMERS_STORAGE[customer_id].name} {CUSTOMERS_STORAGE[customer_id].surname}"
    product_list = []
    
    new_order = {
        "order_id": order_id,
        "customer_id": customer_id,
        "customer_name": customer_name,
        "product_list": product_list
    }

    ORDERS_STORAGE.append(new_order)
    
    return new_order


@router.patch("/{customer_id}/orders/{order_id}/add-products")
async def add_product_to_order(customer_id: int, order_id: int, product_id: int):
    try:
        order_list = [order for order in ORDERS_STORAGE if order["customer_id"] == customer_id]
        if not order_list:
            raise HTTPException(status_code=404, detail="Customer not found")

        if order_id <= 0 or order_id > len(order_list):
            raise HTTPException(status_code=404, detail="Order not found")

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
    order_list = [order for order in ORDERS_STORAGE if order.get("customer_id") == customer_id]
    
    for order in order_list:
        if order["order_id"] == order_id:
            return order
    
    raise HTTPException(status_code=404, detail="Order not found")