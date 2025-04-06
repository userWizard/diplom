from django.db import models

from app.common.models import TimeBaseModel
from app.products.models.categories import Categories

class Products(TimeBaseModel):
    title = models.CharField(
        max_length=100,
        verbose_name='Наименование',
    )
    category = models.ForeignKey(
        Categories,
        verbose_name='Categories',
        related_name='products_categories',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество продукта',
        default=1,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        default='',
    )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

