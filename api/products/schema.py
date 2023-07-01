from pydantic import BaseModel
from typing import Optional, Union

class ProductCreateSchema(BaseModel):
    name: str
    price: float

    class Config:
        schema_extra = {
            "example": {
                "name": "Spaghetti",
                "price": 19.00,
            }
        }

class Product(ProductCreateSchema):
    id: int

class ProductUpdateSchema(BaseModel):
    name: Optional[Union[str, None]]
    price: Optional[Union[float, None]]

    class Config:
        schema_extra = {
            "example": {
                "name": "Spaghetti",
                "price": 19.00,
            }
        }