from django.shortcuts import redirect

from orders.signals import send_order_confirmation
from .models import Order


def payment_return(request):
	try:
		if request.user.is_authenticated:
			last_order = Order.objects.filter(user=request.user).latest('created_at')
			
			if last_order and last_order.paid:
				# Отправляем подтверждение заказа
				return redirect('suces payments views')
			else:
				return redirect('fail payments views')
		else:
			# Handle the case where the user is not authenticated
			return redirect('login')  # Replace with your login page URL
	except Order.DoesNotExist:
		return redirect('order:failure_page')  # Replace with a suitable URL for this case
