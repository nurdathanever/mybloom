from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ReviewForm
from products.models import Product
from .models import Review
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@login_required
def submit_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        rating = data.get('rating')
        comment = data.get('comment')

        product = get_object_or_404(Product, id=product_id)
        review = Review.objects.create(
            user=request.user,
            product=product,
            rating=rating,
            comment=comment
        )
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def get_reviews(request, product_id):
    reviews = Review.objects.filter(product_id=product_id).order_by('-created_at')
    data = [{
        'user': review.user.get_full_name(),
        'rating': review.rating,
        'comment': review.comment,
        'date': review.created_at.strftime("%d %b %Y")
    } for review in reviews]
    return JsonResponse({'reviews': data}, safe=False)