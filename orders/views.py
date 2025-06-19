from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseForbidden
from cart.models import CartItem
from orders.models import Order, OrderItem
from django.utils.dateformat import DateFormat
import random, string
from accounts.models import PaymentCard

@login_required
def start_checkout(request):
    if request.method == "POST":
        request.session["use_bonus"] = request.POST.get("use_bonus") == "true"
        request.session["final_total"] = float(request.POST.get("final_total", 0))
        return redirect("checkout_shipping")


def generate_order_number():
    return ''.join(random.choices(string.digits, k=10))

def checkout_shipping(request):
    if request.method == "POST":
        request.session["shipping"] = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "phone": request.POST.get("phone"),
            "street": request.POST.get("street"),
            "building": request.POST.get("building"),
            "apartment": request.POST.get("apartment"),
            "delivery_method": request.POST.get("delivery_method"),
            "comment": request.POST.get("comment"),
            "date": request.POST.get("date"),
            "time": request.POST.get("time"),
        }
        return redirect("checkout_payment")
    return render(request, "orders/shipping_delivery.html")

@login_required
def checkout_payment(request):
    if request.method == "POST":
        request.session["payment"] = {
            "card_number": request.POST.get("card_number"),
            "card_name": request.POST.get("card_name"),
            "expiry": request.POST.get("expiry"),
            "cvv": request.POST.get("cvv"),
        }
        return redirect("checkout_confirmation")
    cards = PaymentCard.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "orders/payment.html", {
        "cards": cards,
    })

def checkout_confirmation(request):
    shipping = request.session.get("shipping", {})
    payment = request.session.get("payment", {})
    cart_items = CartItem.objects.filter(user=request.user).select_related('product', 'custom_bouquet').prefetch_related('custom_bouquet__flowers__product', 'custom_bouquet__accessories__product')
    cart_summary = []
    total = request.session["final_total"]
    for item in cart_items:
        name = ""
        if item.product:
            name = item.product.name
        elif item.custom_bouquet:
            name = item.custom_bouquet.description
        cart_summary.append({
            "name": name,
            "quantity": item.quantity,
            "total_price": int(item.total_price())
        })

    print(f"Total: {total}")
    if request.method == "POST":
        order = Order.objects.create(
            order_number=generate_order_number(),
            user=request.user,
            name=shipping.get("name"),
            email=shipping.get("email"),
            phone=shipping.get("phone"),
            street=shipping.get("street"),
            building=shipping.get("building"),
            apartment=shipping.get("apartment"),
            delivery_method=shipping.get("delivery_method"),
            comment=shipping.get("comment"),
            delivery_date=shipping.get("date"),
            delivery_time=shipping.get("time"),
            total=total
        )

        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product if cart_item.product else None,
                custom_bouquet=cart_item.custom_bouquet if cart_item.custom_bouquet else None,
                quantity=cart_item.quantity,
                price=int(cart_item.total_price())
            )

            # Decrease stock for standard products
            if cart_item.product:
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
                cart_item.product.sales += cart_item.quantity
                cart_item.product.save()

            # Decrease stock for custom bouquet components
            if cart_item.custom_bouquet:
                for flower in cart_item.custom_bouquet.flowers.all():
                    flower.product.stock -= flower.quantity
                    flower.product.save()
                for accessory in cart_item.custom_bouquet.accessories.all():
                    accessory.product.stock -= 1  # Assuming each accessory is counted once
                    accessory.product.save()

        # Update user total_spent and bonus
        request.user.total_spent += total
        request.user.save()
        request.user.bonus.add_points(int(total * request.user.get_cashback_percentage() / 100))

        # Clear cart and session
        cart_items.delete()
        request.session.pop("shipping", None)
        request.session.pop("payment", None)

        return redirect("order_complete")

    return render(request, "orders/confirmation.html", {
        "shipping": shipping,
        "payment": payment,
        "cart_items": cart_summary,
        "total": total
    })

def order_complete(request):
    return render(request, "orders/order_complete.html")

@login_required
def order_detail_api(request, order_id):
    order = Order.objects.select_related('user').prefetch_related('items__product', 'items__custom_bouquet').get(id=order_id, user=request.user)
    items = order.items.select_related('product', 'custom_bouquet')

    item_data = []
    for item in items:
        if item.product:
            item_data.append({
                "name": item.product.name,
                "price": item.price * item.quantity,
                "image": item.product.image.url if item.product.image else "",
            })
        elif item.custom_bouquet:
            item_data.append({
                "name": item.custom_bouquet.description or "Custom Bouquet",
                "price": item.price * item.quantity,
                "image": item.custom_bouquet.image.url if item.custom_bouquet.image else "",
            })

    response = {
        "order_number": order.order_number,
        "date": DateFormat(order.ordered_at).format('d M Y'),
        "status": order.status,
        "street": order.street,
        "building": order.building,
        "apartment": order.apartment,
        "items": item_data,
        "total": order.total,
    }
    return JsonResponse(response)

@login_required
@require_POST
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        if order.status.lower() == 'delivered':
            order.delete()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"error": "Only delivered orders can be deleted."}, status=403)
    except Order.DoesNotExist:
        return HttpResponseForbidden("You cannot delete this order.")