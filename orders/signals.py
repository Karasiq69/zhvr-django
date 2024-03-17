from django.conf import settings
from django.core.mail import send_mail
import requests

from users.models import UserAccount


def send_order_confirmation(order):
	order_items = order.items.all()
	#TODO помыть это говно
	
	# items_detail = "\n".join([
	# 	f"{item.quantity} x {item.product.title} ({item.attribute if item.attribute else ''}), {item.price} руб."
	# 	for item in order_items])
	
	items_detail = "\n".join([
		f"{item.quantity} x {item.product.title}, {item.price} руб."
		for item in order_items])
	
	subject = f'Заказ №{order.id}: {len(order_items)} товаров на сумму {order.total_cost} рублей'
	message = f'Ваш заказ №{order.id} успешно оформлен.\n\nДетали заказа:\n{items_detail}\n\nОбщая стоимость: {order.total_cost} рублей'
	
	send_mail(
		subject,
		message,
		settings.EMAIL_HOST_USER,
		[order.user.email],
		fail_silently=False,
	)
	
	# Отправка копии письма на внутренний адрес
	send_mail(
		f"Копия: {subject}",
		message,
		settings.EMAIL_HOST_USER,
		['order_bin@zharim-varim.top'],
		fail_silently=False,
	)
	
	try:
		send_order_confirmation_to_telegram(order)
	except Exception as e:
		print(e)


# Пример использования
def send_order_confirmation_to_telegram(order):
	# Получение всех OrderItem, связанных с заказом
	order_items = order.items.all()
	
	# Составление списка товаров с их количеством и стоимостью
	items_detail = "\n".join([
		f"{item.quantity} x {item.product.title}, {item.price} руб."
		for item in order_items])
	
	address = order.address.address + order.address.place if order.address else 'Самовывоз'
	user = UserAccount.objects.get(id=order.user_id)
	
	telegram_message = (
		f'Новый заказ №{order.id}\n'
		f'Имя клиента: {order.user.first_name}\n'
		f'E-mail клиента: {order.user.email}\n'
		f'Номер телефона клиента: {user.phone}\n'
		f'Комментарий: {order.comment}\n'
		f'Адрес: {address}\n'
		f'\nДетали заказа:\n{items_detail}\n'
		f'\nОбщая стоимость: {order.total_cost} рублей'
	)
	
	# Отправка сообщения в Telegram
	send_telegram_message(telegram_message)


def send_telegram_message(message):
	bot_token = '6749870127:AAHGnIC5wOkde6B6QlxfdNZiiITG3J_pnkc'
	chat_id = '-1002077242704'
	url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
	payload = {
		"chat_id": chat_id,
		"text": message
	}
	response = requests.post(url, json=payload)
	return response.json()
