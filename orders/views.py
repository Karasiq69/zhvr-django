from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes

from products.models import Product
from .models import Order, Address, OrderItem
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated]
	
	def perform_create(self, serializer):
		serializer.save(customer=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
	User = get_user_model()
	user = request.user
	data = request.data
	
	order_items = data['order_items']
	address_data = data['address']
	address, created = Address.objects.get_or_create(
		zipcode=address_data['zipcode'],
		city=address_data.get('city', 'Москва'),
		address=address_data['address'],
		place=address_data['place'],
		user=user,
		defaults={'address_name': address_data.get('address_name', '')}
	)
	
	order = Order.objects.create(
		user=user,
		total_cost=data['total_cost'],
		comment=data['comment'],
		order_type=data['order_type'],
		status=data['status'],
		address=address,
		payment_method=data['payment_method']
	)
	
	for item_data in order_items:
		product = Product.objects.get(pk=item_data['id'])
		OrderItem.objects.create(
			order=order,
			product=product,
			quantity=item_data['quantity'],
			price=product.regular_price,
		)
	import time
	if data['payment_method']=='card':
		time.sleep(10)
	
	serializer = OrderSerializer(order)
	return Response(serializer.data)