import logging
from typing import List, Dict, Any

from ninja import Router
from django.http import HttpRequest
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404

from app.application.api.carts.shemas import CartsOutShema
from app.products.models.producst import Products
from app.carts.models import Carts
from app.customers.models import Customers

router = Router(tags=['Carts'])

logger = logging.getLogger('carts')

@router.post('add_product_to_cart/{product_id}', response=CartsOutShema, operation_id='add_product_to_cart')
def add_product_to_cart(request: HttpRequest, product_id: int) -> CartsOutShema:
    try:
        user = request.user
        if not isinstance(user, Customers):
            logger.error(f"Unauthenticated user tried to access cart")
            raise HttpError(401, "Требуется авторизация")

        product = get_object_or_404(Products, pk=product_id)
        
        cart_item = Carts.objects.filter(user=user, product=product).exists()
        
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
            message = "Количество товара увеличено"
            logger.info(f"User {user.id} updated product {product_id} quantity to {cart_item.quantity}")
        else:
            cart_item = Carts.objects.create(
                user=user,
                product=product,
                quantity=1
            )
            message = "Товар добавлен в корзину"
            logger.info(f"User {user.id} added product {product_id} to cart")
        
        return {
            'success': True,
            'message': message,
            'data': {
                'cart_item_id': cart_item.id,
                'quantity': cart_item.quantity
            }
        }
    except Exception as e:
        logger.error(f"Error in add_to_cart: {str(e)}")
        raise HttpError(500, "Ошибка при добавлении в корзину")


@router.delete('delete_product_from_cart/{product_id}', response=CartsOutShema, operation_id='delete_product_from_cart')
def delete_product_from_cart(request: HttpRequest, product_id: int) -> CartsOutShema:
    try:
        user = request.user
        if not isinstance(user, Customers):
            logger.error(f"Unauthenticated user tried to modify cart")
            raise HttpError(401, "Требуется авторизация")

        cart_item = Carts.objects.filter(user=user, product_id=product_id).first()
        
        if not cart_item:
            logger.error(f"Product {product_id} not found in cart for user {user.id}")
            raise HttpError(404, "Товар не найден в корзине")
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            message = "Количество товара уменьшено"
            logger.info(f"User {user.id} decreased product {product_id} quantity to {cart_item.quantity}")
        else:
            cart_item.delete()
            message = "Товар удалён из корзины"
            logger.info(f"User {user.id} removed product {product_id} from cart")
        
        return {
            'success': True,
            'message': message,
            'data': {
                'removed': cart_item.quantity == 0 if hasattr(cart_item, 'quantity') else True
            }
        }

    except Exception as e:
        logger.error(f"Error in remove_from_cart: {str(e)}")
        raise HttpError(500, "Ошибка при удалении из корзины")

@router.get('/items', response=List[CartsOutShema], operation_id='get_cart_items')
def get_cart_items(request: HttpRequest) -> List[CartsOutShema]:
    try:
        user = request.user
        if not isinstance(user, Customers):
            logger.error(f"Unauthenticated user tried to access cart")
            raise HttpError(401, "Требуется авторизация")

        cart_items = Carts.objects.filter(
            user=user
        ).select_related('product').order_by('-created_at')

        if not cart_items.exists():
            logger.info(f"User {user.id} has empty cart")
            return []
        
        logger.info(f"User {user.id} requested cart items")
        return list(cart_items)

    except Exception as e:
        logger.error(f"Error in get_cart_items: {str(e)}")
        raise HttpError(500, "Ошибка при получении корзины")


@router.get('/summary', response=Dict[str, Any], operation_id='get_cart_summary')
def get_cart_summary(request: HttpRequest) -> Dict[str, Any]:
    """
    Возвращает сводную информацию о корзине
    """
    try:
        user = request.user
        if not isinstance(user, Customers):
            logger.error(f"Unauthenticated user tried to access cart summary")
            raise HttpError(401, "Требуется авторизация")

        from django.db.models import Sum, F
        summary = Carts.objects.filter(
            user=user
        ).aggregate(
            total_items=Sum('quantity'),
            total_price=Sum(F('product__price') * F('quantity'))
        )

        result = {
            'total_items': summary['total_items'] or 0,
            'total_price': float(summary['total_price'] or 0),
            'user_id': user.id
        }
        
        logger.info(f"User {user.id} requested cart summary: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in get_cart_summary: {str(e)}")
        raise HttpError(500, "Ошибка при получении сводной информации")