from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from auth_app.models import User  # Предполагаем, что модель User находится в приложении auth_app
from .models import Product, Order


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Guitar",
            description="A test guitar for unit tests",
            price=999.99,
            category="electric",
            image=SimpleUploadedFile("test_image.jpg", b"file_content"),
        )

    def test_product_creation(self):
        """Проверяем, что продукт создается корректно."""
        self.assertEqual(self.product.name, "Test Guitar")
        self.assertEqual(self.product.description, "A test guitar for unit tests")
        self.assertEqual(self.product.price, 999.99)
        self.assertEqual(self.product.category, "electric")
        self.assertEqual(self.product.image.name, "product_images/test_image.jpg")

    def test_product_str_method(self):
        """Проверяем метод __str__ у модели Product."""
        self.assertEqual(str(self.product), "Test Guitar")

    def test_product_category_choices(self):
        """Проверяем, что поле category использует правильные варианты."""
        self.assertEqual(self.product.get_category_display(), "Электрогитара")

        # Проверяем, что недопустимое значение вызывает ошибку
        with self.assertRaises(ValueError):
            Product.objects.create(
                name="Invalid Category",
                description="Test",
                price=100,
                category="invalid_category",
                image=SimpleUploadedFile("test_image.jpg", b"file_content"),
            )


class OrderModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

        # Создаем тестовый продукт
        self.product = Product.objects.create(
            name="Test Guitar",
            description="A test guitar for unit tests",
            price=999.99,
            category="electric",
            image=SimpleUploadedFile("test_image.jpg", b"file_content"),
        )

        # Создаем тестовый заказ
        self.order = Order.objects.create(
            products={"product_id": self.product.id, "quantity": 1},
            ordered_date=timezone.now(),
            user=self.user,
            status="registration",
        )

    def test_order_creation(self):
        """Проверяем, что заказ создается корректно."""
        self.assertEqual(self.order.products, {"product_id": self.product.id, "quantity": 1})
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.status, "registration")
        self.assertIsInstance(self.order.ordered_date, timezone.datetime)

    def test_order_str_method(self):
        """Проверяем метод __str__ у модели Order."""
        self.assertEqual(str(self.order), str(self.order.ordered_date))

    def test_order_status_choices(self):
        """Проверяем, что поле status использует правильные варианты."""
        self.assertEqual(self.order.get_status_display(), "Оформление заказа")

        # Проверяем, что недопустимое значение вызывает ошибку
        with self.assertRaises(ValueError):
            Order.objects.create(
                products={"product_id": self.product.id, "quantity": 1},
                ordered_date=timezone.now(),
                user=self.user,
                status="invalid_status",
            )

    def test_order_user_relationship(self):
        """Проверяем связь между заказом и пользователем."""
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.user.orders_set.count(), 1)
        self.assertEqual(self.user.orders_set.first(), self.order)