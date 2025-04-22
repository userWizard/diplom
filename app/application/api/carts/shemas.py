from ninja import Schema
from datetime import datetime

from app.application.api.products.schemas import ProductInSchema
from app.application.api.customers.schemas import MeOutShema

class CartsOutShema(Schema):
    id: int
    product: 'ProductInSchema'
    user: 'MeOutShema'
    quantity: int
    created_at: datetime
    updated_at: datetime

class CartsInSchema(Schema):
    id: int
    quantity: int