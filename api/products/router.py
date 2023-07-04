from fastapi import APIRouter, HTTPException
from .storage import get_products_storage
from .schema import ProductCreateSchema, ProductUpdateSchema, Product

router = APIRouter()

PRODUCTS_STORAGE = get_products_storage()

@router.post("/")
async def create_product(product: ProductCreateSchema) -> Product:
    for existing_product in PRODUCTS_STORAGE.values():
        if existing_product.name == product.name:
            raise HTTPException(status_code=400, detail="Product already exists.")
    
    if PRODUCTS_STORAGE:
        product_id = max(list(PRODUCTS_STORAGE.keys())) + 1
    else:
        product_id = 1
    new_product = Product(**product.dict(), id=product_id)
    PRODUCTS_STORAGE[product_id] = new_product

    return new_product


@router.get("/")
async def get_products() -> list[Product]:
    return list(get_products_storage().values())


@router.get("/{product_id}")
async def get_product(product_id: int) -> Product:
    try:
        return PRODUCTS_STORAGE[product_id]
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Product with ID={product_id} does not exist.")
    

@router.patch("/{product_id}")
async def update_product(product_id: int, updated_product: ProductUpdateSchema) -> Product:
    new_product = PRODUCTS_STORAGE[product_id]
    updated_data = updated_product.dict(exclude_unset=True)
    for field, value in updated_data.items():
        setattr(new_product, field, value)
    return new_product


@router.delete("/{product_id}")
async def delete_product(product_id: int) -> None:
    try:
        del PRODUCTS_STORAGE[product_id]
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Product with ID={product_id} does not exist."
        )
