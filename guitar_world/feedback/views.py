from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from django.core.mail import send_mail
from .forms import FeedbackForm
from .models import Quest, Chat

class FeedbackFormAPIView(APIView):
    def get(self, request):
        return render(request, "feedback/feedback_form.html", context={"form": FeedbackForm()})
    
    def post(self, request):
        form = FeedbackForm(request.POST)
        if not form.is_valid():
            return render(request, "feedback/feedback_form.html", context={"form": FeedbackForm(), "error": form.error})
        
        quest = Quest.objects.create(
            email=form.cleaned_data["email"],
            question=form.cleaned_data["question"]
        )

        send_mail(
            'Форма обратной связи',
            f'Ваш запрос по номером {quest.id} зарегистрирован. Ответ придёт на эту почту',
            'guitar.world.project.23@gmail.com',
            [form.cleaned_data["email"]],
        )

        return render(request, "feedback/feedback_form.html", context={"form": FeedbackForm(), "error": "Вопрос зарегистрированн"})
    
class FeedbackChatAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/auth/login")
        chat = Chat.objects.filter(user=request.user)
        chat_exists = chat.exists()

        if chat_exists:
            chat = chat.first()
            result_messages = []
            for message in chat.messages:
                is_my_message = message.split("__")[0] == str(request.user.id)
                result_messages.append({"text": chat.messages[message], "classText": "my" if is_my_message else "other", "classParentDiv": "my-parent-div" if is_my_message else ""})
            chat.messages = result_messages
            print(chat.messages)

        return render(request, "feedback/feedback_chat.html", context={"room_name": request.user.id, "chat": chat, "chat_exists": chat_exists})