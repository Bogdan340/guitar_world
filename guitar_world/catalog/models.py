from django.db import models

class Product(models.Model):
    PRODUCT_CHOICES = (
        ("electric", "Электрогитара"),
        ("acoustic", "Акустическая гитара"),
        ("classical", "Классическая гитара"),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=64, choices=PRODUCT_CHOICES)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_ORDER_CHOICES = (
        ("registration", "Оформление заказа"),
        ("dedlivery", "Доставка заказа"),
        ("done", "Заказ выполнен"),
    )
    products = models.JSONField(null=True)
    ordered_date = models.DateTimeField()
    user = models.ForeignKey('auth_app.User', on_delete=models.CASCADE, null=True, blank=True, related_name='orders_set')
    status = models.CharField(choices=STATUS_ORDER_CHOICES, max_length=32)

    def __str__(self):
        return f"{self.ordered_date}"