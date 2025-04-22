from django.db import models
from django.db.models import Sum, F

from app.products.models.producst import Products
from app.common.models import TimeBaseModel
from app.customers.models import Customers

class Carts(TimeBaseModel):
    user = models.OneToOneField(
        Customers,
        on_delete=models.CASCADE,
        related_name='customers_cart',
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name='products_cart',
    )
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    @classmethod
    def get_user_cart_total(cls, user):
        return cls.objects.filter(user=user).aggregate(
            total_quantity=Sum('quantity'),
            total_price=Sum(F('product__price') * F('quantity')
            ))
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
        ordering = ('-quantity',)
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                name='cart_list',
            ),
        ]
