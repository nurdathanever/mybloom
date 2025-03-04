from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("customer", "Customer"),
        ("delivery", "Delivery Person"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Bonus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="bonus")
    points = models.PositiveIntegerField(default=0)

    def add_points(self, amount):
        self.points += amount
        self.save()

    def redeem_points(self, amount):
        if self.points >= amount:
            self.points -= amount
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.user.username} - {self.points} points"