from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("customer", "Customer"),
        ("delivery", "Delivery Person"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    building = models.CharField(max_length=10, blank=True, null=True)
    apartment = models.CharField(max_length=10, blank=True, null=True)
    photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    total_spent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username

    def get_cashback_percentage(self):
        if self.total_spent >= 450000:
            return 15
        elif self.total_spent >= 300000:
            return 10
        elif self.total_spent >= 150000:
            return 5
        return 1


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


class PaymentCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_cards')
    name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=19)
    expiry = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.card_number[-4:]})"


@receiver(post_save, sender=User)
def create_user_bonus(sender, instance, created, **kwargs):
    if created:
        Bonus.objects.create(user=instance)