from django.db import models
from django.db.models import Sum
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
	slug = models.SlugField(max_length=255, blank=True)
	regular_price = models.DecimalField(max_digits=6, decimal_places=2)
	discount_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
	weight = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
	is_active = models.BooleanField(default=True)
	attribute_values = models.ManyToManyField('AttributeValue', blank=True)
	sku = models.CharField(max_length=10, unique=True)
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	
	def get_price(self):
		attribute_price = self.attribute_values.aggregate(total_price=Sum('price'))['total_price']
		if attribute_price is None:
			attribute_price = 0
		return self.regular_price + attribute_price
	
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


class Attribute(models.Model):
	name = models.CharField(max_length=100)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes')
	
	def __str__(self):
		return self.name


class AttributeValue(models.Model):
	attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
	value = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	
	def __str__(self):
		return f'{self.attribute.name} |  {self.value} | {self.price}'
