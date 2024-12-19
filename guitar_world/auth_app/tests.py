from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from catalog.models import Order
from .models import EmailCodes
import uuid


class UserModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            city="Test City",
            street="Test Street",
            house="123",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.city, "Test City")
        self.assertEqual(self.user.street, "Test Street")
        self.assertEqual(self.user.house, "123")
        self.assertEqual(self.user.cart, {"cart": []})
        self.assertFalse(self.user.verify_email)


class EmailCodesModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_email_codes_creation(self):
        email_code = EmailCodes.objects.create(
            id=uuid.uuid4(),
            user=self.user,
            type="resetpassword",
        )
        self.assertEqual(email_code.user, self.user)
        self.assertEqual(email_code.type, "resetpassword")
        self.assertIsInstance(email_code.id, uuid.UUID)

    def test_email_codes_choices(self):
        email_code = EmailCodes.objects.create(
            id=uuid.uuid4(),
            user=self.user,
            type="emailverify",
        )
        self.assertEqual(email_code.type, "emailverify")

        with self.assertRaises(ValueError):
            EmailCodes.objects.create(
                id=uuid.uuid4(),
                user=self.user,
                type="invalid_type",
            )