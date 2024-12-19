from django.urls import path
from .views import (MainPageAPIView,
                    OrdersPageAPIView,
                    ProductsPageAPIView,
                    UpdatePrductPageAPIView,
                    QuestionPageAPIView,
                    QuestPageAPIView,
                    ChatsPageAPIView,
                    ChatPageAPIView,
                    ProductsDeleteAPIView,
                    ProductsCreateAPIView)

urlpatterns = [
    path("", MainPageAPIView.as_view(), name="admin_panel"),
    path("orders", OrdersPageAPIView.as_view(), name="orders-admin-panel"),
    path("products", ProductsPageAPIView.as_view(), name="products"),
    path("products/delete/<int:id>", ProductsDeleteAPIView.as_view(), name="product_delete"),
    path("products/create/", ProductsCreateAPIView.as_view(), name="product_create"),
    path("products/update/<int:id>", UpdatePrductPageAPIView.as_view(), name="product_update"),
    path("chats", ChatsPageAPIView.as_view(), name="feedback-chats"),
    path("chat/<int:id>", ChatPageAPIView.as_view(), name="feedback-chat"),
    path("question", QuestionPageAPIView.as_view(), name="question"),
    path("quest/<int:id>", QuestPageAPIView.as_view(), name="quest"),
]
