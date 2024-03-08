from django.urls import path
from .views import  ProductsByCategoryListView

urlpatterns = [
    # path('products-by-category/', CategoryListView.as_view(), name='products-by-category'),
	path('products-by-category/', ProductsByCategoryListView.as_view(), name='products-by-category'),

]
