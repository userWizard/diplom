from django.db import models

from app.products.models.producst import Products
from app.common.models import TimeBaseModel
from app.project.settings import main as main_settings

class Carts(TimeBaseModel):
    user = models.OneToOneField(
        main_settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart',
    )
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartsProduct(TimeBaseModel):
    cart = models.ForeignKey(
        Carts,
        on_delete=models.CASCADE,
        related_name='items',
    )
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = 'CartProduct'
        verbose_name_plural = 'CartsProducts'
        unique_together = ('cart', 'product')