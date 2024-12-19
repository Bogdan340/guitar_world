from django.test import TestCase
from auth_app.models import User  # Замените на ваш реальный путь к модели User
from .models import Chat, Quest


class ChatModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")

    def test_chat_creation(self):
        chat = Chat.objects.create(
            user=self.user,
            messages={"sender": "testuser", "text": "Hello, world!"}
        )
        self.assertEqual(chat.user, self.user)
        self.assertEqual(chat.messages, {"sender": "testuser", "text": "Hello, world!"})

    def test_chat_user_deletion(self):
        # Создаем объект Chat
        chat = Chat.objects.create(
            user=self.user,
            messages={"sender": "testuser", "text": "Hello, world!"}
        )
        self.user.delete()
        with self.assertRaises(Chat.DoesNotExist):
            Chat.objects.get(id=chat.id)


class QuestModelTest(TestCase):
    def setUp(self):
        self.quest = Quest.objects.create(
            email="test@example.com",
            question="What is the meaning of life?",
            answer="42"
        )

    def test_quest_creation(self):
        self.assertEqual(self.quest.email, "test@example.com")
        self.assertEqual(self.quest.question, "What is the meaning of life?")
        self.assertEqual(self.quest.answer, "42")

    def test_quest_str_method(self):
        self.assertEqual(str(self.quest), "test@example.com")

    def test_quest_answer_null(self):
        quest_without_answer = Quest.objects.create(
            email="noanswer@example.com",
            question="Why is the sky blue?"
        )
        self.assertIsNone(quest_without_answer.answer)