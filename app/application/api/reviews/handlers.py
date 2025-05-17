import logging
from typing import List
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404

from ninja import Router

from app.products.models.producst import Products
from app.products.models.reviews import Reviews
from app.customers.models import Customers
from app.application.api.reviews.shemas import ReviewOutShema, ReviewsInSchema

router = Router(tags=['Reviews'])

logger = logging.getLogger('reviews')


@router.get('{product_id}/get_reviews', response=ReviewsInSchema, operation_id='get_reviews')
def get_reviews(request: HttpRequest, product_id: int) -> List[ReviewOutShema]:
    try:
        product = get_object_or_404(Products, pk=product_id)
        reviews = Reviews.objects.filter(product=product).select_related('customer') 

        logger.info(f"Retrieved {len(reviews)} reviews for product {product_id}")
        return list(reviews)

    except Reviews.DoesNotExist as e:
        logger.error(f"Error fetching reviews for product {product_id}: {str(e)}")
        raise HttpError(500, "Ошибка при получении отзывов")


@router.post('{product_id}/create_reviews', response=ReviewsInSchema,  operation_id='create_reviews')
def create_reviews(request: HttpRequest, product_id: int, review_data: ReviewsInSchema) -> ReviewOutShema:
    try:
        user = request.user

        if not isinstance(user, Customers):
            logger.warning(f"Unauthorized review attempt by user {user.id}")
            raise HttpError(401, "Требуется авторизация")
        
        product = get_object_or_404(Products, pk=product_id)

        if Reviews.objects.filter(customer=user, product=product).exists():
            logger.warning(f"Duplicate review attempt by user {user.id} for product {product_id}")
            raise HttpError(400, "Вы уже оставляли отзыв на этот товар")
        
        # if not user.carts.filter(products=product).exists():
        #     raise HttpError(403, "Вы не можете оставить отзыв на некупленный товар")

        review = Reviews.objects.create(
            customer=user,
            product=product,
            rating=review_data.rating,
            text=review_data.text
        )
        
        logger.info(f"User {user.id} created review {review.id} for product {product_id}")
        return review

    except HttpError:
        raise
    except Exception as e:
        logger.error(f"Error creating review for product {product_id}: {str(e)}")
        raise HttpError(500, "Ошибка при создании отзыва")