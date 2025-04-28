from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CartItem
from products.models import Product
from yourwish.models import CustomBouquetFlower, CustomBouquetAccessory

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related("custom_bouquet")
    enriched_items = []

    for item in cart_items:
        bouquet = item.custom_bouquet
        flowers = CustomBouquetFlower.objects.filter(bouquet=bouquet).select_related("product")
        accessories = CustomBouquetAccessory.objects.filter(bouquet=bouquet).select_related("product")
        enriched_items.append({
            "item": item,
            "image": bouquet.image.url if bouquet and bouquet.image else None,
            "date": item.added_at,
            "flowers": flowers,
            "accessories": accessories,
        })
    print(enriched_items)
    total = sum([item["item"].total_price() for item in enriched_items])

    return render(request, "cart/cart.html", {
        "cart_items": enriched_items,
        "total": total
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect("view_cart")

@login_required
def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect("view_cart")