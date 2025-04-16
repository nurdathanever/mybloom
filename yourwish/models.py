from django.db import models
from django.conf import settings
from products.models import Product

class CustomBouquet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ai_bouquets/')
    description = models.TextField()
    greeting_message = models.TextField(blank=True, null=True)
    postcard = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={"category": "postcard"})
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CustomBouquet #{self.id} by {self.user.username}"

    def calculate_total(self):
        total = 0
        total += sum(flower.product.price * flower.quantity for flower in self.flowers.all())
        total += sum(acc.product.price for acc in self.accessories.all())
        if self.postcard:
            total += self.postcard.price
        return total


class CustomBouquetFlower(models.Model):
    bouquet = models.ForeignKey(CustomBouquet, on_delete=models.CASCADE, related_name='flowers')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, limit_choices_to={"category": "flower"})
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"


class CustomBouquetAccessory(models.Model):
    bouquet = models.ForeignKey(CustomBouquet, on_delete=models.CASCADE, related_name='accessories')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, limit_choices_to={"category__in": ["wrapping_paper", "ribbon"]})
    accessory_type = models.CharField(max_length=20)  # wrapping_paper or ribbon

    def __str__(self):
        return f"{self.accessory_type}: {self.product.name}"