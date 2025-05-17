from datetime import datetime

from pydantic import BaseModel, field_validator

class ReviewsInSchema(BaseModel):
    rating: int
    text: str

    @field_validator('rating')
    def validate_rating(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Рейтинг должен быть от 1 до 5')
        return v


class ReviewOutShema(ReviewsInSchema):
    id: int  # noqa
    customer_id: int
    product_id: int
    created_at: datetime
    updated_at: datetime | None