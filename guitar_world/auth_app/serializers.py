from rest_framework.serializers import ModelSerializer
from .models import User

class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]