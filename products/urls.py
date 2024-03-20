from django.urls import path
from .views import ProductsByCategoryListView, import_products

urlpatterns = [
    # path('products-by-category/', CategoryListView.as_view(), name='products-by-category'),
	path('products-by-category/', ProductsByCategoryListView.as_view(), name='products-by-category'),
	path('import-products/', import_products, name='import_products'),

]
