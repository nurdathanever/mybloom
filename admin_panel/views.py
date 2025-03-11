from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from products.models import Product
from orders.models import Order
from accounts.models import User

# Only allow admins to access
def admin_required(user):
    return user.is_authenticated and user.role == "admin"

@login_required
@user_passes_test(admin_required)
def admin_dashboard(request):
    """Render the custom admin dashboard with product, order, and user statistics."""
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    recent_orders = Order.objects.prefetch_related("items__product").order_by("-ordered_at")[:5]

    return render(request, "admin_panel/dashboard.html", {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "recent_orders": recent_orders,
    })


@login_required
@user_passes_test(admin_required)
def update_order_status(request, order_id):
    """Update order status from admin panel."""
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()
        messages.success(request, "Order status updated successfully!")

    return redirect("admin_dashboard")