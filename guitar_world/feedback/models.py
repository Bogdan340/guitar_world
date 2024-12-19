from django.db import models
from auth_app.models import User

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    messages = models.JSONField()

class Quest(models.Model):
    email = models.EmailField(max_length=128)
    question = models.TextField()
    answer = models.TextField(null=True)

    def __str__(self):
        return self.email