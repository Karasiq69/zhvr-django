from django.db import models

from django.db import models
from pytils.translit import slugify


class Category(models.Model):
	name = models.CharField(
		verbose_name='Название категории', help_text='Обязательное поле', max_length=255, unique=True)
	slug = models.SlugField(max_length=255, unique=True, blank=True)
	is_active = models.BooleanField(default=True)
	
	class Meta:
		verbose_name = ('Категория')
		verbose_name_plural = ('Категории')
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		return super().save(*args, **kwargs)
	
	def __str__(self):
		return self.name


class Product(models.Model):
	title = models.CharField(max_length=255)
	category = models.ForeignKey(Category, on_delete=models.RESTRICT)
	description = models.TextField(blank=True)
	slug = models.SlugField(max_length=255, blank=True, unique=True)
	regular_price = models.DecimalField(max_digits=6, decimal_places=2)
	discount_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
	is_active = models.BooleanField(default=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		ordering = ['-created_at']
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'
	
	
	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)
	
	def __str__(self):
		return self.title


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
	image = models.ImageField(upload_to='images/', default='images/placeholder.png')
	alt_text = models.CharField(max_length=255, null=True, blank=True)
	is_feature = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True, )
	
	def save(self, *args, **kwargs):
		if not self.alt_text:
			self.alt_text = slugify(self.product.title)
		return super().save(*args, **kwargs)
