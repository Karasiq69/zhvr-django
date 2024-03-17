from django.urls import path, include
from rest_framework.routers import DefaultRouter


from products.views import ProductViewSet
from . import views
from .views import OrderViewSet, OrderCreateView, CreateOrderView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
	# path('add/', views.create_order),
	path('add/', CreateOrderView.as_view()),
	path('get-last-order/', views.get_last_order),
	

]
urlpatterns += router.urls