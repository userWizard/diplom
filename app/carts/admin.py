from django.contrib import admin

from app.carts.models import Carts, CartsProduct

@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'items_count', 'created_at', 'updated_at')
    search_fields = ('id', 'user__username', 'user__email')
    list_select_related = ('user',)
    empty_value_display = '-пусто-'
    
    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Общая сумма'
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Товаров в корзине'

@admin.register(CartsProduct)
class CartsProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'added_at', 'total_price', 'created_at', 'updated_at')
    search_fields = ('id', 'product__title', 'cart__user__username')
    list_select_related = ('product', 'cart__user')
    empty_value_display = '-пусто-'
    
    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Сумма'
