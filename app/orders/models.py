from django.db import models

from app.common.models import TimeBaseModel
from app.products.models.producst import Products
from app.customers.models import Customers

class Orders(TimeBaseModel):
    customer = models.ForeignKey(
        Customers,
        verbose_name='Customer',
        on_delete=models.CASCADE,
        related_name='customer_order'
    )
    product = models.ForeignKey(
        Products,
        verbose_name='Product',
        on_delete=models.CASCADE,
        related_name='product_order'
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        unique_together = (
            ('customer', 'product'),
        )