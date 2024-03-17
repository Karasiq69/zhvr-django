from django.db import transaction
from rest_framework import serializers

from products.models import Product, AttributeValue
from products.serializers import ProductSerializer
from .models import Order, OrderItem, Address
from django.contrib.auth import get_user_model

UserAccount = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = ['id', 'zipcode', 'city', 'address', 'place', 'address_name']


# class AddressSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Address
# 		fields = ['id', 'zipcode', 'city', 'address', 'place', 'address_name', 'is_primary']
# 		read_only_fields = ['id', 'is_primary']
#
# 	def create(self, validated_data):
# 		user = self.context['request'].user
# 		address = Address.objects.create(user=user, **validated_data)
# 		return address
#
# 	def update(self, instance, validated_data):
# 		instance.zipcode = validated_data.get('zipcode', instance.zipcode)
# 		instance.city = validated_data.get('city', instance.city)
# 		instance.address = validated_data.get('address', instance.address)
# 		instance.place = validated_data.get('place', instance.place)
# 		instance.address_name = validated_data.get('address_name', instance.address_name)
# 		instance.save()
# 		return instance


# class OrderItemSpecificationSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = OrderItemSpecification
# 		fields = ('specification', 'value')


class OrderItemSerializer(serializers.ModelSerializer):
	product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
	attribute_values = serializers.PrimaryKeyRelatedField(queryset=AttributeValue.objects.all(), many=True, required=False)
	price = serializers.SerializerMethodField()
	
	class Meta:
		model = OrderItem
		fields = ['id', 'product', 'attribute_values', 'quantity', 'price']
	
	def get_price(self, obj):
		return obj.get_price()


class OrderSerializer(serializers.ModelSerializer):
	# user = serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all(), required=False)
	# address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), required=False)
	items = OrderItemSerializer(many=True)
	address = AddressSerializer()
	
	class Meta:
		model = Order
		fields = ['id', 'address', 'comment', 'total_cost', 'created_at', 'order_type', 'paid',
		          'payment_amount', 'payment_method', 'status', 'items']
	
	def create(self, validated_data):
		items_data = validated_data.pop('items')
		address_data = validated_data.pop('address')
		user = self.context['request'].user  # Получение пользователя из request
		
		address = user.addresses.first()
		if address:
			for key, value in address_data.items():
				setattr(address, key, value)
			address.save()
		else:
			address = Address.objects.create(user=user, **address_data)
		
		order = Order.objects.create(user=user, address=address, **validated_data)
		
		for item_data in items_data:
			product = item_data['product']
			quantity = item_data['quantity']
			attribute_values = item_data.get('attribute_values', [])
			print('attribute_values', attribute_values)
			print('quantity', quantity)
			print('product', product)
			# Вычисление цены на основе выбранных атрибутов
			if attribute_values:
				price = sum(attr.price for attr in attribute_values)
			else:
				price = product.regular_price
			
			order_item = OrderItem.objects.create(
				
				order=order,
				
				product=product,
				quantity=quantity,
				price=price  # Присвоение значения полю price
			)
			
			if attribute_values:
				order_item.attribute_values.set(attribute_values)
		
		return order
