from django.contrib.auth import get_user_model
from django.db import models
from products.models import Product

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=20, default="")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    ordered_at = models.DateTimeField(auto_now_add=True)

    # New Fields
    ai_bouquet_image = models.ImageField(upload_to="ai_bouquets/", blank=True, null=True)
    greeting_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Optional: Greeting card message per item (if needed)
    custom_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"