from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.decorators.cache import cache_page

from .models import Product
from .forms import ProductForm, ProductFilterForm
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.is_authenticated and user.role == "admin"

@cache_page(60 * 1)
def product_list(request):
    all_flower_types = Product.objects.filter(category='flower').distinct()
    all_bouquets = Product.objects.filter(category='bouquet').order_by('-sales')

    # Mark top 3 as bestseller
    top3_ids = list(all_bouquets.values_list('id', flat=True)[:3])
    for product in all_bouquets:
        product.is_bestseller = product.id in top3_ids

    # Sort remaining by discount
    sorted_products = sorted(all_bouquets, key=lambda p: (-p.sales if p.id in top3_ids else 0, -p.discount))

    form = ProductFilterForm(request.GET)
    if form.is_valid():
        filters = Q()
        if form.cleaned_data['flower_ingredients']:
            filters &= Q(flower_ingredients__name__in=form.cleaned_data['flower_ingredients'])
        if form.cleaned_data['size']:
            filters &= Q(size__in=form.cleaned_data['size'])
        if form.cleaned_data['seasonality']:
            filters &= Q(seasonality__in=form.cleaned_data['seasonality'])
        if form.cleaned_data['style']:
            filters &= Q(style__in=form.cleaned_data['style'])
        filtered_products = Product.objects.filter(category='bouquet').filter(filters).distinct()
        top3_ids = list(filtered_products.order_by('-sales').values_list('id', flat=True)[:3])
        for product in filtered_products:
            product.is_bestseller = product.id in top3_ids
        sorted_products = sorted(filtered_products, key=lambda p: (-p.sales if p.id in top3_ids else 0, -p.discount))

    return render(request, 'products/product_list.html', {
        'products': sorted_products,
        'filter_form': form,
        "all_flower_types": all_flower_types
    })

@cache_page(60 * 1)
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