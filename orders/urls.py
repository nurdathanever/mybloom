from django.urls import path
from . import views

urlpatterns = [
    path('shipping/', views.checkout_shipping, name='checkout_shipping'),
    path('payment/', views.checkout_payment, name='checkout_payment'),
    path('confirmation/', views.checkout_confirmation, name='checkout_confirmation'),
    path('complete/', views.order_complete, name='order_complete'),
    path('api/detail/<int:order_id>/', views.order_detail_api, name='order_detail_api'),

]