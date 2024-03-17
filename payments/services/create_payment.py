from django.conf import settings
from yookassa import Configuration, Payment as YooKassaPayment
from payments.models import Payment as PaymentModel


def create_payment(request, user, amount, order_id):
	Configuration.account_id = settings.PAYMENT_SHOP_ID
	Configuration.secret_key = settings.PAYMENT_SECRET_KEY
	session_id = request.session.session_key
	return_url = settings.KASSA_RETURN_URL + '/checkout/payment-return/'
	# Создание платежа
	payment = YooKassaPayment.create({
		"amount": {
			"value": str(amount),
			"currency": "RUB"
		},
		"confirmation": {
			"type": "redirect",
			"return_url": return_url
		},
		"metadata": {
			"user_id": user.id,
			"order_id": order_id,
			"session_id": session_id,
		},
		"capture": True,
		"description": f"Оплата заказа {user.email}"
	})
	
	PaymentModel.objects.create(
		user=user,
		order_id=order_id,
		amount=amount,
		status=payment.status,
		payment_id=payment.id
	)
	
	return payment
