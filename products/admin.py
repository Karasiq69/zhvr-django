from django.contrib import admin

from products.models import Product, Category, ProductImage

# Register your models here.

# admin.site.register(Category)
# admin.site.register(ProductImage)

from .models import (
	Category,
	Product,
	ProductImage,
)

admin.site.register(Category)


class ProductImageInline(admin.TabularInline):
	model = ProductImage


@admin.register(Product)
class ProductTypeAdmin(admin.ModelAdmin):
	inlines = [
		ProductImageInline,
	]
