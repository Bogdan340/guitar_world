from django.contrib import admin
from .models import User, EmailCodes

# Register your models here.
admin.site.register(User)
admin.site.register(EmailCodes)