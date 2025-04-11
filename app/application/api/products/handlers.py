import logging
from typing import List, Optional

from django.http import HttpRequest
from ninja.security import django_auth
from ninja import Router
from ninja.errors import HttpError

from app.application.api.products.shemas import ProductOutSchema, ProductInSchema
from app.products.models.producst import Products


router = Router(tags=['Products'])

logger = logging.getLogger('products')


@router.get(
    '/products{product_id}',
    responese=ProductOutSchema,
    operation_id='get_by_id',
    auth=django_auth
)
def get_by_id(request: HttpRequest, product_id: int) -> ProductInSchema:
    try: 
        product = Products.objects.get(id=product_id).first()
    except Products.DoesNotExist as e:
        logger.error(f"No product with this id was found: {str(e)}", exc_info=True)
        raise HttpError(400, f'Продукт с указанным id не найден {str(e)}')

    return product


@router.get(
    '/products_list',
    response=List[ProductOutSchema],
    operation_id='get_product_list',
    auth=None
)
def get_products_list(request: HttpRequest) -> ProductInSchema:
    ...


@router.get(
    '/products{title}',
    response=ProductOutSchema,
    operation_id='get_product_by_title',
    auth=django_auth
)
def get_products_by_title(request: HttpRequest, title: Optional[str] = None) -> ProductInSchema:
    try:
        if title is not None:
            product = Products.objects.filter(title__icontains=title)
    except Products.DoesNotExist as e:
        logger.error(f'There is no product with that name: {str(e)}', exc_info=True)
        raise HttpError(400, f'Продукт с указанным именем {title} не найден {str(e)}')

    return product