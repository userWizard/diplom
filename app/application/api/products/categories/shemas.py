from ninja import Schema

from datetime import datetime

class CategoryOutSchema(Schema):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime

class CategoryInSchama(Schema):
    id: int
    title: str