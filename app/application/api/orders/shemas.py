from pydantic import BaseModel

from datetime import datetime


class OrderSchema(BaseModel):
    id: int #noqa
    product: int
    customer: int
    created_at: datetime
    udated_at: datetime| None