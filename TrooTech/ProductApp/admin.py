from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class Articles(admin.ModelAdmin):
    list_display = ("name", "ancestor")


@admin.register(Product)
class Products(admin.ModelAdmin):
    pass
