from django.urls import path

from .services.accept_payment import accept_payment
from .services.create_payment import create_payment
from .views import payment_return


urlpatterns = [
	# User return View
	path('return/', payment_return, name='payment_return'),
	# API return View
	path('api/create_payment/', create_payment, name='yoo-create_payment'),
	path('api/accept_payment/', accept_payment, name='yoo-payment-acceptance')
]
