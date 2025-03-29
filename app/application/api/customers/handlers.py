from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from app.application.api.customers.schemas import (
    GetOrCreateInSchema,
    GetByIdSchema,
    DeleteByIdSchema,
    UpdateCustomerSchema,
    GetOrCreateOutSchema,
    GetByIdOutSchema,
    DeleteByIdOutSchema,
    UpdateCustomerOutSchema,
)
from app.customers.entities.domain import ORMCustomerRepository
from app.common.exceptions import ServiceException

router = Router(tags=['Customers'])


@router.post('get_or_create', response=GetOrCreateOutSchema, operation_id='get_or_create')
def get_or_create(request: HttpRequest, schema: GetOrCreateInSchema) -> GetOrCreateOutSchema:
    customer_repo = ORMCustomerRepository()
    try:
        result = customer_repo.get_or_create(
            name=schema.name,
            email=schema.email,
            phone_number=schema.phone_number,
            password=schema.password,
        )
    except ServiceException as exception:
        raise HttpError(
            status_code=400,
            message=exception.message,
        ) from exception

    return GetOrCreateOutSchema.from_entity(result)


@router.get('{user_id}',response=GetByIdOutSchema, operation_id='get_by_id')
def get_by_id(request: HttpRequest, schema: GetByIdSchema) -> GetByIdOutSchema:
    customer_repo = ORMCustomerRepository()

    try:
        result = customer_repo.get_by_id(user_id=schema.id)
    except ServiceException as exception:
        raise HttpError(
            status_code=400,
            message=exception.message,
        ) from exception

    return GetByIdOutSchema(result)


@router.put('update_customer',responese=UpdateCustomerOutSchema, operation_id='update_customer')
def update_customer(request: HttpRequest, schema: UpdateCustomerSchema) -> UpdateCustomerOutSchema:
    customer_repo = ORMCustomerRepository()

    try:
        result = customer_repo.update_customer(
            email=schema.email,
            password=schema.password,
        )
    except ServiceException as exception:
        raise HttpError(
            status_code=400,
            message=exception.message,
        ) from exception

    return UpdateCustomerOutSchema(result)


@router.delete('{user_id}',response=DeleteByIdOutSchema, operation_id='delete_account')
def delete_customer(request: HttpRequest, schema: DeleteByIdSchema) -> DeleteByIdOutSchema:
    customer_repo = ORMCustomerRepository()
    
    try:
        result = customer_repo.delete_customer(user_id=schema.id)
    except ServiceException as exception:
        raise HttpError(
            status_code=400,
            message=exception.message,
        ) from exception

    return DeleteByIdOutSchema(result)