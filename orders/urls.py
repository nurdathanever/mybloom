from django.urls import path
from . import views

urlpatterns = [
    path('orders/shipping/', views.checkout_shipping, name='checkout_shipping'),
    path('orders/payment/', views.checkout_payment, name='checkout_payment'),
    path('orders/confirmation/', views.checkout_confirmation, name='checkout_confirmation'),
    path('orders/complete/', views.order_complete, name='order_complete'),
]