from django.contrib import admin

from app.products.models.producst import Products
from app.products.models.categories import Categories
from app.products.models.reviews import Reviews


@admin.register(Products)
class ProducstAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'price', 'category', 'quantity', 'description', 'is_available', 'image_url', 'created_at', 'updated_at',
    )
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'created_at', 'updated_at',)
    list_select_related = ('customer', 'product')
    empty_value_display = '-пусто-'