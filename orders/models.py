from django.db import models

from users.models import UserAccount


class Order(models.Model):
	customer = models.ForeignKey(UserAccount, related_name='orders', on_delete=models.CASCADE)
	comment = models.CharField(max_length=255, null=True, blank=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.pk + ' ' + self.customer
