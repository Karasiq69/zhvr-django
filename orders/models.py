from django.db import models

from products.models import Product
from users.models import UserAccount


class Order(models.Model):
	CREATED = 'created'
	ORDERED = 'ordered'
	SHIPPED = 'shipped'
	CANCELED = 'canceled'
	CLOSED = 'closed'
	PENDING = 'pending'
	
	STATUS_CHOICES = (
		(CREATED, 'Создан'),
		(ORDERED, 'Оформлен'),
		(SHIPPED, 'Доставлен'),
		(CANCELED, 'Отменен'),
		(CLOSED, 'Завершен'),
		(PENDING, 'В обработке'),
	)
	
	LOCAL_PICKUP = 'local_pickup'
	DELIVERY = 'delivery'
	
	ORDER_TYPE_CHOICES = (
		(LOCAL_PICKUP, 'Самовывоз'),
		(DELIVERY, 'Доставка'),
	)
	
	PAYMENT_CARD = 'card'
	PAYMENT_CASH = 'cash'
	PAYMENT_SBP = 'sbp'
	
	PAYMENT_METHOD_CHOICES = (
		(PAYMENT_CARD, 'Карта'),
		(PAYMENT_CASH, 'Наличные'),
		(PAYMENT_SBP, 'СБП'),
	)
	
	user = models.ForeignKey(UserAccount, related_name='orders', on_delete=models.CASCADE, blank=True, null=True)
	address = models.ForeignKey('Address', null=True, blank=True, related_name='orders', on_delete=models.SET_NULL)
	comment = models.CharField(max_length=255, null=True, blank=True, )
	total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default=LOCAL_PICKUP)
	paid = models.BooleanField(default=False)
	payment_amount = models.IntegerField(blank=True, null=True)
	payment_method = models.CharField(
		max_length=100,
		choices=PAYMENT_METHOD_CHOICES,
		default=PAYMENT_CASH,
		blank=True
	)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CREATED)
	
	def __str__(self):
		return f"Заказ №{self.id}"


class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
	price = models.IntegerField()
	quantity = models.IntegerField(default=1)
	
	# attribute = models.ForeignKey(DrinkAttribute, on_delete=models.SET_NULL, null=True, blank=True)
	
	def __str__(self):
		return f"{self.product.title} - {self.quantity} шт."
	
	def get_order_item_cost(self):
		return self.price * self.quantity


class Address(models.Model):
	user = models.ForeignKey(UserAccount, related_name='addresses', on_delete=models.CASCADE, blank=True, null=True)
	zipcode = models.CharField(max_length=255, blank=True)
	city = models.CharField(max_length=255, blank=True, default='Москва')
	address = models.CharField(max_length=255, blank=True)
	place = models.CharField(max_length=255, blank=True)
	address_name = models.CharField(max_length=255, blank=True)
	
	is_primary = models.BooleanField(default=False)
	
	def __str__(self):
		return f'{self.address}'
	
	def save(self, *args, **kwargs):
		if not self.pk and not Address.objects.filter(user=self.user).exists():
			self.is_primary = True
		super(Address, self).save(*args, **kwargs)
	
	def set_as_primary(self):
		Address.objects.filter(user=self.user).update(is_primary=False)
		self.is_primary = True
		self.save()
