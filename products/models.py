from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("bouquet", "Bouquet"),
        ("flower", "Flower"),
        ("wrapping_paper", "Wrapping Paper"),
        ("ribbon", "Ribbon"),
        ("postcard", "Postcard"),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)  # Percentage (0-100%)
    stock = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def discounted_price(self):
        return self.price * (1 - self.discount / 100)

    def __str__(self):
        return f"{self.name} - {self.category}"