from django.urls import path
from . import views

urlpatterns = [
    path('', views.flower_picker, name='yourwish_flowers'),
    path('accessories/', views.accessories_picker, name='yourwish_accessories'),
    path('blooming/', views.blooming_screen, name='yourwish_blooming'),
    path('result/', views.bloom_result, name='yourwish_result'),
    path('postcard/', views.postcard_picker, name='yourwish_postcard'),
    path('submit-order/', views.create_order, name='yourwish_create_order'),
]