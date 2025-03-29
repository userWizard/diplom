from ninja import Schema

from datetime import datetime

from app.customers.entities.entities import Customer as CustomerEntity


class  GetOrCreateInSchema(Schema):
    name: str
    email: str
    phone_number: str
    password: str


class GetOrCreateOutSchema(Schema):
    id: int
    name: str
    email: str
    phone_number: str
    password: str
    created_at: datetime

    @classmethod
    def from_entity(cls, customer: CustomerEntity) -> 'GetOrCreateOutSchema':
        return cls(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            phone_number=customer.phone_number,
            password=customer.password,
            created_at=customer.created_at,
        )


class GetByIdSchema(Schema):
    id: int


class GetByIdOutSchema(Schema):
    id: int


class DeleteByIdSchema(Schema):
    id: int


class DeleteByIdOutSchema(Schema):
    id: int


class UpdateCustomerSchema(Schema):
    email: str
    password: str


class UpdateCustomerOutSchema(Schema):
    id: int
    name: str
    email: str