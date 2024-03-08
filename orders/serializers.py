from rest_framework import serializers
from .models import Order
from django.contrib.auth import get_user_model

UserAccount = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
	customer_name = serializers.ReadOnlyField(source='customer.first_name')
	
	class Meta:
		model = Order
		fields = ['id', 'customer', 'customer_name', 'comment', 'created_at']
