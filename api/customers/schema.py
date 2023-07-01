from pydantic import BaseModel
from typing import Optional, Union

class CustomerCreateSchema(BaseModel):
    name: str
    surname: str
    email: str
    phone_number: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Jan",
                "surname": "Kowalski",
                "email": "jan.kowalski@example.com",
                "phone_number": "000-000-000"
            }
        }


class CustomerUpdateSchema(BaseModel):
    name: Optional[Union[str, None]]
    surname: Optional[Union[str, None]]
    email: Optional[Union[str, None]]
    phone_number: Optional[Union[str, None]]

    class Config:
        schema_extra = {
            "example": {
                "name": "Leszek"
            }
        }


class Customer(CustomerCreateSchema):
    id: int
