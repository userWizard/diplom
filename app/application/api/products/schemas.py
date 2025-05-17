from datetime import datetime

from pydantic import BaseModel

from app.application.api.products.categories.shemas import CategoryInSchama


class ProductInSchema(BaseModel):
    title: str

class ProductOutSchema(ProductInSchema):
    id: int # noqa
    quantity: int
    price: float
    category: 'CategoryInSchama'
    description: str
    is_available: bool
    created_at: datetime
    updated_at: datetime

