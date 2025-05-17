from django.db import models

from app.common.models import TimeBaseModel
from app.products.models.producst import Products
from app.customers.models import Customers

class Reviews(TimeBaseModel):
    customer = models.ForeignKey(
        Customers,
        verbose_name='Customers',
        on_delete=models.CASCADE,
        related_name='customers_reviews',
    )
    product = models.ForeignKey(
        Products,
        verbose_name='Products',
        on_delete=models.CASCADE,
        related_name='products_reviews',
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='User rating',
        default=1,
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=255,
        blank=True,
        default='',
    )

    def __str__(self) -> str:
        return self.text

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = (
            ('customer', 'product'),
        )