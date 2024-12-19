from django.db import models
from django.contrib.auth.models import AbstractUser
from catalog.models import Order

class User(AbstractUser):
    orders = models.ManyToManyField(Order, related_name='+')
    verify_email = models.BooleanField(default=False)
    city = models.CharField(max_length=100, null=True)
    street = models.CharField(max_length=100, null=True)
    house = models.CharField(max_length=100, null=True)
    cart = models.JSONField(default={"cart": []})

class EmailCodes(models.Model):
    EMAIL_CODES_CHOICES = (("resetpassword", "Сброс пароля"), ("emailverify", "Потдвердить email"))
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=32, choices=EMAIL_CODES_CHOICES)

        