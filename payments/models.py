from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

from orders.models import Order


class Payment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	status = models.CharField(max_length=50)
	payment_id = models.CharField(max_length=100, unique=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"Payment {self.id} by {self.user}"