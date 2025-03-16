from django.contrib import admin
from app.customers.models.customers import Customers

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'email', 'phone_number', 'password', 'created_at')
    search_fields = ('id', 'email',)
