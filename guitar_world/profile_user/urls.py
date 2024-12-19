from django.urls import path
from .views import ProfileAPIView, CartAPIView, NewOrderAPIView, OrderAPIView

urlpatterns = [
    path('', ProfileAPIView.as_view(), name='profile'),
    path('cart', CartAPIView.as_view(), name='cart'),
    path('neworder', NewOrderAPIView.as_view(), name='neworder'),
    path('order/<int:id>', OrderAPIView.as_view(), name='order'),
]
