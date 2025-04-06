from django.contrib import admin
from app.customers.models import Customers

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'password', 'created_at')
    search_fields = ('id', 'email',)
    empty_value_display = '-пусто-'
