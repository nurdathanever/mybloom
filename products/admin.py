from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "discount", "stock", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("name", "description")

admin.site.register(Product, ProductAdmin)