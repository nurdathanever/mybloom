from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.is_authenticated and user.role == "admin"

def product_list(request):
    """Display all products with search and filter options."""
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category:
        products = products.filter(category=category)

    categories = Product.CATEGORY_CHOICES  # Get category choices

    return render(request, "products/product_list.html", {
        "products": products,
        "categories": categories,
        "query": query,
        "selected_category": category,
    })


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