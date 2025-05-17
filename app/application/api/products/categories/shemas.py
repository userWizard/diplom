from pydantic import BaseModel

from datetime import datetime

class CategoryInSchama(BaseModel):
    title: str

class CategoryOutSchema(CategoryInSchama):
    id: int # noqa
    created_at: datetime
    updated_at: datetime

