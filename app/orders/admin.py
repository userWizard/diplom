from django.contrib import admin

from app.orders.models import Orders

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product')
    empty_value_display = '-пусто-'
