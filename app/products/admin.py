from django.contrib import admin

from app.products.models.producst import Products
from app.products.models.categories import Categories


@admin.register(Products)
class ProducstAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'category', 'quantity', 'description', 'created_at', 'updated_at',
    )
    search_fields = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at',)
    search_fields = ('title',)
    empty_value_display = '-пусто-'