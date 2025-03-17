from django.http import HttpRequest
from ninja import Router

router = Router(tags=['Customers'])

@router.post('get_or_create', operation_id='get_or_create')
def get_or_create(request: HttpRequest):
    ...

@router.get('{user_id}', operation_id='get_by_id')
def get_by_id(request: HttpRequest, user_id: int):
    ...

@router.put('{user_id}', operation_id='update_customer')
def update_customer(request: HttpRequest, user_id: int):
    ...

@router.post('auth', operation_id='authorize')
def authorization(request: HttpRequest):
    ...

@router.delete('delete_account', operation_id='delete_account')
def delete_account(request: HttpRequest, user_id: int):
    ...