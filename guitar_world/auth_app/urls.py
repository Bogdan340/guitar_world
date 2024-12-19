from django.urls import path
from .views import LoginAPIView, RegistrationAPIView, ResetPasswordAPIView, VerifyEmailAPIView

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('resetpassword', ResetPasswordAPIView.as_view(), name='resetpassword'),
    path('registration', RegistrationAPIView.as_view(), name='registration'),
    path('verifyemail', VerifyEmailAPIView.as_view(), name='verifyemail'),
]
