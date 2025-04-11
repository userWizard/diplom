from datetime import datetime

from ninja import Schema

from app.application.api.products.categories.shemas import CategoryInSchama

class ProductOutSchema(Schema):
    id: int
    title: str
    quantity: int
    category: 'CategoryInSchama'
    description: str
    created_at: datetime
    updated_at: datetime


class ProductInSchema(Schema):
    id: int
    title: str