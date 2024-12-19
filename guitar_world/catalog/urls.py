from django.urls import path
from .views import IndexAPIView, CatalogAPIView, AddIncartAPIView, ProductDetailAPIView, MinusCartAPIView

urlpatterns = [
    path('', IndexAPIView.as_view(), name='index'),
    path('catalog', CatalogAPIView.as_view(), name='catalog'),
    path('catalog/addincart', AddIncartAPIView.as_view(), name='addincart'),
    path('catalog/minuscart', MinusCartAPIView.as_view(), name='minuscart'),
    path('catalog/product/<int:id>', ProductDetailAPIView.as_view(), name='product_detail'),
]
