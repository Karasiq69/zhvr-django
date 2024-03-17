import json

import requests
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from orders.signals import send_order_confirmation
from payments.models import Payment as PaymentModel

from orders.models import Order


@csrf_exempt
@require_POST
def accept_payment(request):
	print('start accept_payment', request.body)
	try:
		data = json.loads(request.body)
		
		if data.get('event')=='payment.succeeded' and data.get('type')=='notification':
			payment_info = data['object']
			status = payment_info['status']
			
			if status=="succeeded":
				handle_payment_success(payment_info)
				print(payment_info)
			return HttpResponse(status=200)
		
		return HttpResponse(status=200)
	
	except Exception as e:
		print(f"Error processing webhook: {str(e)}")
		return HttpResponse(status=500)


def handle_payment_success(payment_info):
	order_id = payment_info.get('order_id')  # Убедитесь, что такой ключ существует в payment_info
	order = None
	try:
		# Clear the cart if needed
		session_id = payment_info.get('metadata', {}).get('session_id')
		# if session_id:
		# 	session = SessionStore(session_key=session_id)
		# 	session[settings.CART_SESSION_ID] = {}  # Update as per your cart storage logic
		# 	session.save()
		
		# Retrieve and update the order and payment model
		order_id = payment_info.get('metadata', {}).get('order_id')
		print(order_id, 'ЕТО ORDER ID ACCEPT PAYMENT')
		if order_id:
			order = Order.objects.get(id=order_id)
			order.paid = True
			order.payment_amount = float(payment_info['amount']['value'])
			order.payment_method = 'card'
			order.status = Order.ORDERED
			order.save()
			
			send_order_confirmation(order)
			
			payment_id = payment_info['id']
			
			payment_record = PaymentModel.objects.get(payment_id=payment_id)
			payment_record.status = payment_info['status']
			payment_record.order = order
			payment_record.save()
			
			user_id = payment_info['metadata']['user_id']
			requests.post('http://localhost:3000/api/payment-success', json={'user_id': user_id})
	
	
	except Exception as e:
		print(f"Error in handle_payment_success: {str(e)}")
