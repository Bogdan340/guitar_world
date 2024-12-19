from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(label=False, widget=forms.TextInput(attrs={"class": "inp", "id": "email", "type": "email", "name": "email", "placeholder": "Email"}))
    password = forms.CharField(label=False, widget=forms.TextInput(attrs={"class": "inp", "type": "password", "id": "password", "name": "password", "placeholder": "Пароль"}))

class RegistrationForm(forms.Form):
    email = forms.CharField(label=False, widget=forms.TextInput(attrs={"class": "inp", "id": "email", "type": "email", "name": "email", "placeholder": "Email"}))
    password = forms.CharField(label=False, widget=forms.TextInput(attrs={"class": "inp", "type": "password", "id": "password", "name": "password", "placeholder": "Пароль"}))
    password_confirm = forms.CharField(label=False, widget=forms.TextInput(attrs={"class": "inp", "type": "password", "id": "password_confirm", "name": "password", "placeholder": "Повторите пароль"}))

class ResetPasswordForm(forms.Form):
    email = forms.CharField(label=False, widget=forms.TextInput(attrs={"class": "inp", "id": "email", "type": "email", "name": "email", "placeholder": "Email"}))

class ResetPasswordActionForm(forms.Form):
    password = forms.CharField(label=False, widget=forms.TextInput(attrs={"class": "inp", "id": "password", "type": "text", "name": "password", "placeholder": "Новый пароль"}))
