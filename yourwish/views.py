import base64
import logging
import os
from io import BytesIO
from datetime import datetime
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page

from products.models import Product
from cart.models import CartItem
from django.utils import timezone
from yourwish.models import CustomBouquet, CustomBouquetFlower, CustomBouquetAccessory
from openai import OpenAI
from django.conf import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)


@login_required
@cache_page(60 * 5)
def yourwish_tabs(request):
    step = request.POST.get("step", "flowers")
    selected_flowers = request.session.get("selected_flowers", {})
    wrapping_paper_id = request.session.get("wrapping_paper")
    ribbon_id = request.session.get("ribbon")
    message = request.session.get("message", "")
    postcard_id = request.session.get("postcard_id")

    if request.method == "POST":
        current_step = request.POST.get("step")
        if current_step == "flowers":
            flower_data = {}
            for key in request.POST:
                if key.startswith("flowers_"):
                    flower_id = key.replace("flowers_", "")
                    try:
                        quantity = int(request.POST[key])
                        if quantity > 0:
                            flower_data[flower_id] = quantity
                    except (ValueError, TypeError):
                        continue
            request.session["selected_flowers"] = flower_data
            step = "accessories"

        elif current_step == "accessories":
            request.session["wrapping_paper"] = request.POST.get("wrapping_paper")
            request.session["ribbon"] = request.POST.get("ribbon")
            step = "postcard"

        elif current_step == "postcard":
            request.session["postcard_id"] = request.POST.get("postcard_id")
            request.session["message"] = request.POST.get("message", "")
            return redirect("yourwish_bloomit")

    flowers = Product.objects.filter(category='flower', stock__gt=0)
    papers = Product.objects.filter(category='wrapping_paper')
    ribbons = Product.objects.filter(category='ribbon')
    postcards = Product.objects.filter(category='postcard')

    return render(request, "yourwish/yourwish_tabs.html", {
        "step": step,
        "flowers": flowers,
        "papers": papers,
        "ribbons": ribbons,
        "cards": postcards,
        "selected_flowers": selected_flowers,
        "wrapping_paper_id": wrapping_paper_id,
        "ribbon_id": ribbon_id,
        "message": message,
        "postcard_id": postcard_id
    })


@cache_page(60 * 5)
@login_required
def yourwish_bloomit(request):
    flowers_data_str = request.POST.get("flowers_data", "{}")
    flowers_data = json.loads(flowers_data_str)
    print(flowers_data)

    selected_flowers = flowers_data.get("flowers", {})
    wrapping_paper_id = flowers_data.get("wrapping_paper")
    ribbon_id = flowers_data.get("ribbon")
    message = flowers_data.get("message", "")

    wrapping = Product.objects.filter(id=wrapping_paper_id, category="wrapping_paper").first()
    ribbon = Product.objects.filter(id=ribbon_id, category="ribbon").first()

    flower_parts = []
    for flower_id, qty in selected_flowers.items():
        flower = Product.objects.filter(id=flower_id).first()
        if flower and qty > 0:
            flower_parts.append(f"exactly {qty} {flower.name} stems")
    flower_str = ", ".join(flower_parts)

    prompt = (
        f"A realistic close-up of a minimalistic bouquet with {flower_str}, elegantly arranged and rich in color "
        f"and detail. Wrapped in {wrapping.name} wrapping paper and tied with a {ribbon.name} ribbon bow. Soft natural daylight, "
        f"gentle shadows, neutral blurred background. Vertical shot, shallow depth of field, "
        f"magazine-style floral photography."
    )
    print(prompt)

    response = client.images.generate(model="dall-e-3", prompt=prompt,
                                      n=1,
                                      size="1024x1024",
                                      response_format="b64_json")
    img_data = base64.b64decode(response.data[0].b64_json)
    img = Image.open(BytesIO(img_data))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_filename = f"media/ai_bouquets/preview_{request.user.id}_{timestamp}.jpeg"
    os.makedirs(os.path.dirname(img_filename), exist_ok=True)
    img.save(img_filename, format="JPEG")

    request.session["ai_bouquet_image"] = f"ai_bouquets/preview_{request.user.id}_{timestamp}.jpeg"

    # Preserve bouquet session data
    if request.method == "POST":
        request.session["flowers"] = selected_flowers
        request.session["wrapping_paper"] = wrapping_paper_id
        request.session["ribbon"] = ribbon_id
        request.session["message"] = message

    return render(request, "yourwish/bloom_result.html", {
        "image_url": f"/media/ai_bouquets/preview_{request.user.id}_{timestamp}.jpeg"
    })


@cache_page(60 * 5)
@login_required
def yourwish_confirm_bouquet(request):
    print(request.session.keys())
    print(request.session.values())
    selected_flowers = {int(k): int(v) for k, v in request.session.get("flowers", {}).items() if v > 0}
    wrapping_paper_id = int(request.session.get("wrapping_paper")) if request.session.get("wrapping_paper") else None
    ribbon_id = int(request.session.get("ribbon")) if request.session.get("ribbon") else None
    postcard_id = int(request.session.get("postcard_id")) if request.session.get("postcard_id") else None
    message = request.session.get("message")
    print(f"message: {message}")
    bouquet_image = request.session.get("ai_bouquet_image", "ai_bouquets/sample_bouquet.jpeg")

    import random
    adjectives = ["Blossoming", "Radiant", "Velvet", "Ethereal", "Golden", "Serene"]
    nouns = ["Dream", "Whispers", "Charm", "Elegance", "Symphony", "Delight"]
    flower_names = [Product.objects.get(id=flower_id).name for flower_id in selected_flowers.keys()]
    flower_part = ", ".join(flower_names) if flower_names else "Bouquet"
    bouquet_description = f"{random.choice(adjectives)} {random.choice(nouns)} with {flower_part}"

    total_price = 0

    custom_bouquet = CustomBouquet.objects.create(
        user=request.user,
        image=bouquet_image,
        description=bouquet_description,
        greeting_message=message,
        postcard=Product.objects.filter(id=postcard_id, category='postcard').first() if postcard_id else None,
        total_price=0
    )

    for flower_id, qty in selected_flowers.items():
        try:
            flower = Product.objects.get(id=flower_id, category='flower')
            CustomBouquetFlower.objects.create(
                bouquet=custom_bouquet,
                product=flower,
                quantity=qty
            )
            total_price += flower.price * qty
            print(f"Flowers price: {total_price}")
        except Product.DoesNotExist as e:
            logging.error(e.args)
            continue

    if wrapping_paper_id:
        try:
            paper = Product.objects.get(id=wrapping_paper_id, category='wrapping_paper')
            CustomBouquetAccessory.objects.create(
                bouquet=custom_bouquet,
                product=paper,
                accessory_type="wrapping_paper"
            )
            total_price += paper.price
            print(f" + Wrapping price: {total_price}")

        except Product.DoesNotExist as e:
            logging.error(e.args)
            pass

    if ribbon_id:
        try:
            ribbon = Product.objects.get(id=ribbon_id, category='ribbon')
            CustomBouquetAccessory.objects.create(
                bouquet=custom_bouquet,
                product=ribbon,
                accessory_type="ribbon"
            )
            total_price += ribbon.price
            print(f" + Ribbon price: {total_price}")
        except Product.DoesNotExist as e:
            logging.error(e.args)
            pass

    if custom_bouquet.postcard:
        total_price += custom_bouquet.postcard.price
        print(f" + postcard price: {total_price}")

    print(f"Final calculated total price: {total_price}")
    custom_bouquet.total_price = total_price
    custom_bouquet.save()

    CartItem.objects.create(
        user=request.user,
        custom_bouquet=custom_bouquet,
        quantity=1,
        added_at=timezone.now()
    )

    for key in ["selected_flowers", "wrapping_paper", "ribbon", "message", "postcard_id"]:
        request.session.pop(key, None)

    return redirect("view_cart")
