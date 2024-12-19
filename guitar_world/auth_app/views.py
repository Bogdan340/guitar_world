from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from .serializers import RegistrationSerializer
from .forms import LoginForm, RegistrationForm, ResetPasswordForm, ResetPasswordActionForm
from .models import User, EmailCodes
import re
import uuid
from django.core.mail import send_mail

class LoginAPIView(APIView):
    def get(self, request: HttpRequest):
        return render(request, 'auth/login.html', context={"form": LoginForm(), "error": ""})
    
    def post(self, request: HttpRequest):
        post = request.POST
        form = LoginForm(post)

        if not form.is_valid():
            return render(request, 'auth/login.html', context={"form": LoginForm(), "error": form.errors})
        
        user = auth.authenticate(username=post.get("email"), password=post.get("password"))

        if user is None:
            return render(request, 'auth/login.html', context={"form": LoginForm(), "error": "Пользователь не найден"})
        
        if not user.verify_email:
            return render(request, 'auth/login.html', context={"form": LoginForm(), "error": "Почта не подтверждена"})
        
        auth.login(request, user)
        
        return HttpResponseRedirect('/')
    
class RegistrationAPIView(APIView):
    def get(self, request: HttpRequest):
        return render(request, 'auth/registration.html', context={"form": RegistrationForm(), "error": ""})
    
    def post(self, request: HttpRequest):
        error = ""
        post = request.POST

        reg = RegistrationForm(post)

        if not reg.is_valid():
            return render(request, 'auth/registration.html', context={"form": RegistrationForm(), "error": reg.error_messages})
        
        newUser = RegistrationSerializer(data={
            "username": post.get("email"),
            "email": post.get("email"),
            "password": make_password(post.get("password"))
        })

        if not newUser.is_valid():
            return render(request, 'auth/registration.html', context={"form": RegistrationForm(), "error": newUser.error_messages})
        
        newUser.save()

        verifyemail = EmailCodes.objects.create(id=uuid.uuid4(), user=User.objects.filter(email=newUser.data["email"])[0], type="emailverify")

        send_mail(
            'Потверждение почты',
            f'Для потверждение почты перейдите по ссылке: http://127.0.0.1/auth/verifyemail?uuid={verifyemail.id}',
            'guitar.world.project.23@gmail.com',
            [post.get('email')],
        )

        return render(request, 'auth/registration.html', context={"form": RegistrationForm(), "error": "", "message": "Письмо для потверждения почты отправлено"})
    
class ResetPasswordAPIView(APIView):
    def get(self, request: HttpRequest):
        get = request.GET

        if get.get("uuid") is None:
            return render(request, 'auth/resetpassword.html', context={"form": ResetPasswordForm(), "error": ""})
        if not EmailCodes.objects.filter(id=get.get("uuid")).exists():
            return HttpResponseRedirect('/auth/resetpassword')
        
        code = EmailCodes.objects.filter(id=get.get("uuid")).first()

        if code.type != "resetpassword":
            return HttpResponseRedirect('/')

        return render(request, 'auth/resetpasswordaction.html', context={"form": ResetPasswordActionForm(), "uuid": get.get("uuid"), "error": ""})
    
    def post(self, request: HttpRequest):
        post = request.POST

        if post.get("typeaction") == "resetpassword" and not post.get("uuid") is None:
            code = EmailCodes.objects.filter(id=post.get("uuid"))

            if not code.exists():            
                return render(request, 'auth/resetpassword.html', context={"form": ResetPasswordForm(), "error": "Ошибка"})
            
            user = User.objects.get(id=code.first().user.id)
            user.password = make_password(post.get("password"))
            user.save()
            code.delete()
            return render(request, 'auth/resetpassword.html', context={"form": ResetPasswordForm(), "message": "Пароль успешно изменен"})

        if re.compile(r"^\S+@\S+\.\S+$").match(post.get("email", "")) is None:
            return render(request, 'auth/resetpassword.html', context={"form": ResetPasswordForm(), "error": "Email не валиден"})

        if User.objects.filter(email=post.get("email")).exists():
            user = User.objects.get(email=post.get("email"))
            code = EmailCodes.objects.create(id=uuid.uuid4(), user=user, type="resetpassword")
            send_mail(
                'Сброс пароля',
                f'Для сброса пароля перейдите по ссылке: http://127.0.0.1/auth/resetpassword?uuid={code.id}',
                'guitar.world.project.23@gmail.com',
                [post.get('email')],
                fail_silently=False,
            )

        return render(request, 'auth/resetpassword.html', context={"form": ResetPasswordForm(), "error": ""})
    
class VerifyEmailAPIView(APIView):
    def get(self, request: HttpRequest):
        uuid = request.GET.get("uuid")

        if not EmailCodes.objects.filter(id=uuid).exists():
            return render(request, 'auth/succesverify.html')
        
        code = EmailCodes.objects.filter(id=uuid).first()

        if code.type != "emailverify":
            return HttpResponseRedirect('/')

        user = User.objects.get(id=code.user.id)
        user.verify_email = True
        user.save()

        code.delete()

        return render(request, 'auth/succesverify.html', context={"message": "Почта успешно подтверждена"})