from django import forms

class FeedbackForm(forms.Form):
    email = forms.CharField(label="", widget=forms.EmailInput(attrs={"class": "inp", "type": "email", "id": "email", "name": "email", "placeholder": "example@example.com"}), max_length=128)
    question = forms.CharField(label="", widget=forms.Textarea(attrs={"class": "inp textarea", "id": "question", "name": "question"}), max_length=8192)