from rest_framework import serializers

from products.models import Product
from .models import Order, OrderItem, Address
from django.contrib.auth import get_user_model

UserAccount = get_user_model()


class OrderItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderItem
		fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
	customer_name = serializers.ReadOnlyField(source='customer.first_name')
	order_items = serializers.SerializerMethodField()
	
	
	class Meta:
		model = Order
		fields = '__all__'
	
	def get_order_items(self, obj):
		items = obj.items.all()  # Используем related_name для доступа к элементам заказа
		serializer = OrderItemSerializer(items, many=True)
		return serializer.data
	
	def create(self, validated_data):
		items_data = validated_data.pop('items')
		order = Order.objects.create(**validated_data)
		
		for item_data in items_data:
			OrderItem.objects.create(order=order, **item_data)
