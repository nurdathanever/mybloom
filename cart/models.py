from django.db import models
from django.conf import settings
from products.models import Product
from yourwish.models import CustomBouquet

class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    custom_bouquet = models.ForeignKey("yourwish.CustomBouquet", null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        if self.custom_bouquet:
            return self.quantity * self.custom_bouquet.total_price
        elif self.product:
            return self.quantity * self.product.price
        return 0