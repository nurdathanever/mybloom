from django.db import models
from accounts.models import User
from orders.models import Order

class Delivery(models.Model):
    delivery_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'delivery'})
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery")
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, default="pending")
    estimated_delivery_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Delivery for Order {self.order.id} - {self.status}"