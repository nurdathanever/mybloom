from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.is_authenticated and user.role == "admin"

def product_list(request):
    products = Product.objects.filter(category='bouquet')

    # Filters
    flower_type = request.GET.get("flower_type")
    size = request.GET.get("size")
    seasonality = request.GET.get("seasonality")
    style = request.GET.get("style")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort")

    if flower_type:
        products = products.filter(flower_ingredients__name__icontains=flower_type)

    if size:
        products = products.filter(size=size)

    if seasonality:
        products = products.filter(seasonality=seasonality)

    if style:
        products = products.filter(style=style)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if sort == "rating":
        products = products.order_by("-rating")  # add rating field later
    elif sort == "arrival":
        products = products.order_by("-created_at")
    elif sort == "sale":
        products = products.order_by("-discount")
    elif sort == "bestselling":
        products = products.order_by("-sales")  # add sales field later

    flower_types = Product.objects.filter(category="flower").values_list("name", flat=True).distinct()

    context = {
        "products": products,
        "flower_types": flower_types,
    }
    return render(request, "products/product_list.html", context)


def product_detail(request, product_id):
    """Display details of a single product."""
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})

@login_required
@user_passes_test(is_admin)
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("product_list")
    return render(request, "products/product_form.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect("product_list")
    return render(request, "products/product_form.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "products/product_confirm_delete.html", {"product": product})