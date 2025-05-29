import logging
import re
from typing import List
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from app.application.api.products.schemas import ProductOutSchema, ProductInSchema
from app.products.models.producst import Products


router = Router(tags=['Products'])

logger = logging.getLogger('products')


@router.get(
    'products/{product_id}',
    response=ProductInSchema,
    operation_id='get_by_id',
)
def get_by_id(request: HttpRequest, product_id: int) -> ProductOutSchema:
    user = request.user
    if not user.is_authenticated:
            raise HttpError(401, "Требуется авторизация")
    try: 
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist as e:
        logger.error(f"No product with this id was found: {str(e)}", exc_info=True)
        raise HttpError(400, f'Продукт с указанным id не найден {str(e)}')

    return product


@router.get(
    'products_list/',
    response=List[ProductInSchema],
    operation_id='get_product_list',
)
def get_products_list(request: HttpRequest) -> ProductOutSchema:
    try:
        products = Products.objects.all()
        return list(products)
    except Products.DoesNotExist as e:
        logger.error(f"Server not found: {str(e)}", exc_info=True)
        raise HttpError(500, f'Оишбка сервера {str(e)}')


@router.get(
    'products_by_name/',
    response=List[ProductInSchema],
    operation_id='get_product_by_title',
)
def get_products_by_title(request: HttpRequest, title: str, limit: int = 20, offset: int = 0) -> List[ProductOutSchema]:
    try:
        search_query = ' '.join(title.strip().lower().split())
        
        type_query = r'(^|\s)' + re.escape(search_query) + r'(\s|$)'

        products = Products.objects.filter(
            title__iregex=type_query
        )[offset:offset+limit]

        if not products.exists():
            products = Products.objects.filter(
                title__icontains=search_query
            )[offset:offset+limit]
        
        if not products.exists():
            raise HttpError(404, f'Продукты с названием "{title}" не найдены')
            
        return list(products)
    
    except Exception as e:
        logger.error(f'Error fetching products: {str(e)}', exc_info=True)
        raise HttpError(500, 'Ошибка при получении продуктов')