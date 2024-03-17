from django.contrib import admin
from .models import Order, OrderItem, Product, Address


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 1


class OrderAdmin(admin.ModelAdmin):
	inlines = [OrderItemInline, ]
	list_display = ['__str__', 'total_cost', 'created_at', 'status']


admin.site.register(Order, OrderAdmin)


# class OrderItemSpecificationInline(admin.TabularInline):
#     model = OrderItemSpecification
#     extra = 1

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('id', 'order', 'product', 'price', 'quantity')
	# inlines = [OrderItemSpecificationInline]


admin.site.register(Address)
# admin.site.register(OrderItemSpecification)
