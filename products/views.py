from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Product
from .serializers import ProductSerializer, ProductsByCategorySerializer

from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer
from django.contrib import messages
from django.shortcuts import redirect
from .services.product_importer import main


class ProductViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	
	def get_permissions(self):
		if self.action in ['list', 'retrieve']:
			permission_classes = [AllowAny]
		else:
			permission_classes = [IsAuthenticatedOrReadOnly]
		return [permission() for permission in permission_classes]


class CategoryListView(generics.ListAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = [AllowAny]


class ProductsByCategoryListView(generics.ListAPIView):
	queryset = Category.objects.all()
	serializer_class = ProductsByCategorySerializer
	permission_classes = [AllowAny]


from django.contrib import messages
from django.shortcuts import redirect
from .services.product_importer import main


def import_products(request):
	if request.method=='GET':
		try:
			main()
			messages.success(request, 'Импорт данных выполнен успешно.')
		except Exception as e:
			messages.error(request, f'Ошибка при импорте данных: {str(e)}')
	return redirect('admin:index')
