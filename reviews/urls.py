from django.urls import path
from .views import submit_review, get_reviews

urlpatterns = [
    path('api/add_review/', submit_review, name='submit_review'),
    path('api/get_reviews/<int:product_id>/', get_reviews, name='get_reviews'),
]