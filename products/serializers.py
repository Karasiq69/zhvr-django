from rest_framework.permissions import AllowAny

from .models import Product, ProductImage,  Attribute, AttributeValue
from rest_framework import serializers
from .models import Category, Product


class ImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = ['image', 'alt_text']
	
	def get_image(self, obj):
		request = self.context.get('request')
		if obj.image and hasattr(obj.image, 'url'):
			image_url = obj.image.url
			return request.build_absolute_uri(image_url) if request else image_url
		return None


# class ProductSpecificationValueSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = ProductSpecificationValue
# 		fields = ('specification', 'value', 'price')


class AttributeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Attribute
		fields = ['id', 'name', 'category']


class AttributeValueSerializer(serializers.ModelSerializer):
	attribute = AttributeSerializer()
	
	class Meta:
		model = AttributeValue
		fields = ['id', 'attribute', 'value', 'price']


class ProductSerializer(serializers.ModelSerializer):
	product_image = ImageSerializer(many=True, read_only=True)
	# specifications = ProductSpecificationValueSerializer(many=True, source='productspecificationvalue_set')
	# attributes = serializers.DictField(required=False)
	attribute_values = AttributeValueSerializer(many=True)
	# attributes = AttributeSerializer(many=True)
	
	class Meta:
		model = Product
		fields = ['id', 'title', 'description', 'regular_price', 'discount_price', 'slug', 'product_image', 'category',
		          'weight',  'attribute_values']


class CategorySerializer(serializers.ModelSerializer):
	products = ProductSerializer(many=True, read_only=True)
	
	class Meta:
		model = Category
		fields = ['id', 'name', 'products']


class ProductsByCategorySerializer(serializers.ModelSerializer):
	products = serializers.SerializerMethodField()
	
	class Meta:
		model = Category
		fields = "__all__"
		permission_classes = [AllowAny]  # Разрешить доступ всем пользователям
	
	
	def get_products(self, instance):
		request = self.context.get('request')
		products = instance.product_set.filter(is_active=True)
		return ProductSerializer(products, many=True, context={'request': request}).data
