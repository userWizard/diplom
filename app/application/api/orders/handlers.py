import logging
from typing import List
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404

from ninja import Router

from app.products.models.producst import Products
from app.customers.models import Customers
from app.application.api.orders.shemas import OrderSchema


router = Router(tags=['Orders'])

logger = logging.getLogger('orders')

@router.post('{product_id}/add_product_to_order', response=OrderSchema, operation_id='add_product_to_order')
def add_product_to_order(request: HttpRequest, product_id: int) -> OrderSchema:
    pass
