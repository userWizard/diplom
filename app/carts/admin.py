from django.contrib import admin

from app.carts.models import Carts

@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'quantity', 'items_count', 'created_at', 'updated_at')
    search_fields = ('id', 'product__title')
    list_select_related = ('user',)
    empty_value_display = '-пусто-'
    
    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Сумма'

    
    def items_count(self, obj):
        return obj.quantity
    items_count.short_description = 'Товаров в корзине'
