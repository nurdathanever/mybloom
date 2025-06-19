from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from products.models import Product
from products.forms import ProductForm
from orders.models import Order
from accounts.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

# Only allow admins to access
def admin_required(user):
    return user.is_authenticated and user.role == "admin"

@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()

    recent_orders = Order.objects.select_related('user') \
        .prefetch_related('items__product', 'items__custom_bouquet__flowers__product', 'items__custom_bouquet__accessories__product') \
        .order_by('-ordered_at')

    all_fields = list_fields(Order)
    print(all_fields)

    order_data = []
    for order in recent_orders:
        items = order.items.select_related('product', 'custom_bouquet')
        item_list = []

        for item in items:
            if item.product:
                item_list.append({
                    "name": item.product.name,
                    "image": item.product.image.url if item.product.image else "",
                    "count": item.quantity
                })
            elif item.custom_bouquet:
                item_list.append({
                    "name": item.custom_bouquet.description,
                    "image": item.custom_bouquet.image.url if item.custom_bouquet.image else "",
                    "count": item.quantity
                })

        order_data.append({
            "order": order,
            "status": order.status,
            "items": item_list,
        })

    return render(request, "admin_panel/dashboard.html", {
        "current_tab": "orders",
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "recent_orders": order_data,
    })

@staff_member_required
def admin_users(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    users = User.objects.all().order_by('-date_joined')
    return render(request, "admin_panel/dashboard.html", {
        "current_tab": "users",
        "users": users,
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
    })

@staff_member_required
def admin_products(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    products = Product.objects.all().order_by('-created_at')
    return render(request, "admin_panel/dashboard.html", {
        "current_tab": "products",
        "products": products,
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
    })

def list_fields(model, prefix="", visited=None):
    if visited is None:
        visited = set()

    if model in visited:
        return []  # prevent infinite loop

    visited.add(model)
    fields = []

    for field in model._meta.get_fields():
        if field.is_relation and field.related_model:
            if field.many_to_many or field.one_to_many:
                continue  # Skip reverse/redundant relations
            fields.extend(list_fields(field.related_model, f"{prefix}{field.name}__", visited))
        else:
            fields.append(f"{prefix}{field.name}")

    return fields

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

@login_required
@require_POST
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(request.POST, request.FILES, instance=product)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("admin_products"))
    return JsonResponse({"success": False, "errors": form.errors}, status=400)

@login_required
@require_POST
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
