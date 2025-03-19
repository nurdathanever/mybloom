from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from products.models import Product
from orders.models import Order, OrderItem


def flower_picker(request):
    flowers = Product.objects.filter(category='flower', stock__gt=0)
    return render(request, 'yourwish/flower_picker.html', {'flowers': flowers})

def accessories_picker(request):
    if request.method == "POST":
        selected_flower_ids = request.POST.getlist('flowers')
        request.session['yourwish_flowers'] = selected_flower_ids
    papers = Product.objects.filter(category='wrapping_paper')
    ribbons = Product.objects.filter(category='ribbon')
    return render(request, 'yourwish/accessories_picker.html', {'papers': papers, 'ribbons': ribbons})

def blooming_screen(request):
    if request.method == "POST":
        selected_papers = request.POST.get('wrapping_paper')
        selected_ribbons = request.POST.get('ribbon')
        request.session['yourwish_paper'] = selected_papers
        request.session['yourwish_ribbon'] = selected_ribbons
    return render(request, 'yourwish/blooming.html')

def bloom_result(request):
    context = {
        "bouquet_image": "/static/img/sample_bouquet.jpeg"  # placeholder for now
    }
    return render(request, "yourwish/bloom_result.html", context)

def postcard_picker(request):
    postcards = Product.objects.filter(category='postcard')
    return render(request, 'yourwish/postcard_picker.html', {'cards': postcards})

@login_required
def create_order(request):
    selected_flowers = request.session.get("selected_flowers", {})
    wrapping_paper_id = request.session.get("wrapping_paper")
    ribbon_id = request.session.get("ribbon")
    bouquet_image = "ai_bouquets/sample_bouquet.jpeg"  # relative path for ImageField

    # Handle greeting card data
    postcard = None
    message = ""
    if request.method == "POST":
        postcard_id = request.POST.get("postcard_id")
        message = request.POST.get("message", "")
        postcard = Product.objects.filter(id=postcard_id, category="postcard").first()
    elif request.GET.get("skip_card"):
        postcard = None
        message = ""
    else:
        return redirect("yourwish_postcard")

    # Create the order
    order = Order.objects.create(
        user=request.user,
        address="Custom Bouquet",  # You can make this dynamic later
        phone="000000000",
        total_price=0,
        status="pending",  # matches your model's STATUS_CHOICES
        ai_bouquet_image=bouquet_image,
        greeting_message=message
    )

    total_price = 0

    # Add selected flowers
    for flower_id, quantity in selected_flowers.items():
        try:
            flower = Product.objects.get(id=flower_id)
            OrderItem.objects.create(
                order=order,
                product=flower,
                quantity=int(quantity),
                price=flower.price
            )
            total_price += flower.price * int(quantity)
        except Product.DoesNotExist:
            continue

    # Add wrapping paper
    if wrapping_paper_id:
        try:
            paper = Product.objects.get(id=wrapping_paper_id)
            OrderItem.objects.create(order=order, product=paper, quantity=1, price=paper.price)
            total_price += paper.price
        except Product.DoesNotExist:
            pass

    # Add ribbon
    if ribbon_id:
        try:
            ribbon = Product.objects.get(id=ribbon_id)
            OrderItem.objects.create(order=order, product=ribbon, quantity=1, price=ribbon.price)
            total_price += ribbon.price
        except Product.DoesNotExist:
            pass

    # Add postcard (if selected)
    if postcard:
        OrderItem.objects.create(
            order=order,
            product=postcard,
            quantity=1,
            price=postcard.price,
            custom_message=message
        )
        total_price += postcard.price

    # Finalize order price
    order.total_price = total_price
    order.save()

    # Clear session
    request.session.pop("selected_flowers", None)
    request.session.pop("wrapping_paper", None)
    request.session.pop("ribbon", None)

    return render(request, "yourwish/order_success.html", {"order": order})