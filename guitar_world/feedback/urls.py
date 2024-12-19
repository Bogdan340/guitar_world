from django.urls import path
from .views import FeedbackFormAPIView, FeedbackChatAPIView

urlpatterns = [
    path("feedback_form", FeedbackFormAPIView.as_view(), name="feedback_form"),
    path("feedback_chat", FeedbackChatAPIView.as_view(), name="feedback_chat"),
]