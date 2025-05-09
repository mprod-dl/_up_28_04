from django.urls import path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')
router.register('tags', TagViewSet, basename='tags')
router.register('orders', OrderViewSet, basename='orders')
router.register('order-items', OrderItemViewSet, basename='order-items')

urlpatterns = router.urls
