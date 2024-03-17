from django.contrib import admin

# Register your models here.


from .models import (
	Category,
	Product,
	ProductImage,
	# ProductSpecification,
	# ProductSpecificationValue,
	# ProductType,
	AttributeValue, Attribute
)

admin.site.register(Category)

#
# class ProductSpecificationsInline(admin.TabularInline):
# 	model = ProductSpecification
#
#
# @admin.register(ProductType)
# class ProductTypeAdmin(admin.ModelAdmin):
# 	inlines = [
# 		ProductSpecificationsInline,
# 	]


class ProductImageInline(admin.TabularInline):
	model = ProductImage

#
# class ProductSpecificationValueInline(admin.TabularInline):
# 	model = ProductSpecificationValue

@admin.register(Product)
class ProductTypeAdmin(admin.ModelAdmin):
	inlines = [
		# ProductSpecificationValueInline,
		ProductImageInline,
	]

# admin.site.register(ProductSpecificationValue)
# admin.site.register(ProductSpecification)
admin.site.register(AttributeValue)
admin.site.register(Attribute)
