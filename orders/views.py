from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from rest_framework.response import Response

from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes

from payments.services.create_payment import create_payment
from products.models import Product, AttributeValue
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
@permission_classes([AllowAny])
# TODO allow any убрать
def create_order(request):
	print('CREATE ORDER DATA:', request.data)
	serializer = OrderSerializer(data=request.data, context={'request': request})
	if serializer.is_valid():
		order = serializer.save()
		
		if order.payment_method=='card':
			total_amount = order.total_cost
			payment = create_payment(request, request.user, total_amount, order.id)
			
			if payment.confirmation and payment.confirmation.confirmation_url:
				return Response({'url': payment.confirmation.confirmation_url})
			else:
				return Response({'error': 'Ошибка создания платежа'}, status=400)
		
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderCreateView(generics.CreateAPIView):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	
	def create(self, request, *args, **kwargs):
		# Вывод данных запроса перед сериализацией
		print("Request data before serialization:")
		print(request.data)
		
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		# Вывод валидированных данных после сериализации
		print("Validated data after serialization:")
		print(serializer.validated_data)
		
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		
		# Вывод созданного заказа
		print("Created order:")
		print(serializer.data)
		
		return Response(serializer.data, status=201, headers=headers)


@require_http_methods(["GET"])
def get_last_order(request):
	try:
		user = request.user
		last_order = Order.objects.filter(user=user).latest('created_at')
		
		serializer = OrderSerializer(last_order)
		
		return JsonResponse(serializer.data, safe=False)
	except Order.DoesNotExist:
		return JsonResponse({"error": "Заказ не найден"}, status=404)


class CreateOrderView(generics.CreateAPIView):
	serializer_class = OrderSerializer
	
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		order = serializer.save()
		cart_items = request.data.get('cart_items', [])
		for item in cart_items:
			product_id = item['product_id']
			quantity = item['quantity']
			attribute_value_ids = item.get('attribute_value_ids', [])
			
			product = Product.objects.get(id=product_id)
			order_item = OrderItem.objects.create(
				order=order,
				product=product,
				quantity=quantity
			)
			
			if attribute_value_ids:
				attribute_values = AttributeValue.objects.filter(id__in=attribute_value_ids)
				order_item.attribute_values.set(attribute_values)
		
		payment_method = request.data.get('payment_method')
		if payment_method=='card':
			payment = create_payment(request, request.user, order.total_cost, order.id)
			return Response({'url': payment.confirmation.confirmation_url}, status=status.HTTP_201_CREATED)
		
		return Response(serializer.data, status=status.HTTP_201_CREATED)
