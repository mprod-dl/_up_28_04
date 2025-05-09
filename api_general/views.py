from rest_framework import viewsets
from .serializers import *
from general.models import *
from .permissions import CustomPermissions
from rest_framework.pagination import PageNumberPagination

class PaginationPage(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 3

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage

