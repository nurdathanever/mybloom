from django.db import models
from decimal import Decimal

class Product(models.Model):
    CATEGORY_CHOICES = [
        ("bouquet", "Bouquet"),
        ("flower", "Flower"),
        ("wrapping_paper", "Wrapping Paper"),
        ("ribbon", "Ribbon"),
        ("postcard", "Postcard"),
    ]
    BOUQUET_SIZES = [("S", "Small"), ("M", "Medium"), ("L", "Large")]
    SEASONALITY_CHOICES = [("spring", "Spring"), ("summer", "Summer"), ("autumn", "Autumn"), ("winter", "Winter")]
    STYLE_CHOICES = [("classic", "Classic"), ("minimalistic", "Minimalistic"), ("exotic", "Exotic"), ("lush", "Lush"),
                     ("mono", "Mono")]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(default=0)  # Percentage (0-100%)
    stock = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    flower_ingredients = models.ManyToManyField("self", blank=True, symmetrical=False,
                                                limit_choices_to={'category': 'flower'})
    size = models.CharField(max_length=10, choices=BOUQUET_SIZES, blank=True, null=True)
    seasonality = models.CharField(max_length=10, choices=SEASONALITY_CHOICES, blank=True, null=True)
    style = models.CharField(max_length=20, choices=STYLE_CHOICES, blank=True, null=True)

    @property
    def discounted_price(self):
        return self.price * (Decimal('1') - Decimal(self.discount) / Decimal('100'))

    def __str__(self):
        return f"{self.name} - {self.category}"