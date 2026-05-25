from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sku', 'shop', 'location', 'price', 'is_available', 'is_delete')
    list_filter = ('is_available', 'is_delete', 'category')
    search_fields = ('name', 'sku', 'shop')