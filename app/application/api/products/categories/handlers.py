import logging
from typing import List
import re

from ninja import Router
from ninja.errors import HttpError
from django.http import HttpRequest


from app.application.api.products.categories.shemas import (
    CategoryInSchama,
    CategoryOutSchema,
)
from app.products.models.categories import Categories

router = Router(tags=['Categories'])

logger = logging.getLogger('categories')

@router.get('get_all_categories/', response=List[CategoryInSchama], operation_id='get_all_products')
def get_all_categories(request: HttpRequest) -> List[CategoryOutSchema]:
    try:
        category = Categories.objects.all()
        return list(category)
    except Categories.DoesNotExist as e:
        logger.error(f"Server not found: {str(e)}", exc_info=True)
        raise HttpError(500, f'Оишбка сервера {str(e)}')


@router.get('get_catogry_by_name/',  response=List[CategoryInSchama], operation_id='get_catogry_by_name')
def get_catogry_by_name(request: HttpRequest, title: str, limit: int = 20, offset: int = 0) -> List[CategoryOutSchema]:
    try:
        search_query = ' '.join(title.strip().lower().split())
        
        type_query = r'(^|\s)' + re.escape(search_query) + r'(\s|$)'

        categories = Categories.objects.filter(
            title__iregex=type_query
        )[offset:offset+limit]

        if not categories.exists():
            categories = Categories.objects.filter(
                title__icontains=search_query
            )[offset:offset+limit]
        
        if not categories.exists():
            raise HttpError(404, f'Продукты с названием "{title}" не найдены')
            
        return list(categories)
    
    except Exception as e:
        logger.error(f'Error fetching products: {str(e)}', exc_info=True)
        raise HttpError(500, 'Ошибка при получении категорий')
