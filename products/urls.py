from django.urls import path
from .views import ProductListCreateAPIView, ProductDetailUpdateDeleteAPIView

urlpatterns = [
    path('products', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<str:id>/', ProductDetailUpdateDeleteAPIView.as_view(), name='product-detail-update-delete'),
]