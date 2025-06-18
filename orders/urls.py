from django.urls import path
from . import views

urlpatterns = [
    path("start-checkout/", views.start_checkout, name="start_checkout"),
    path('shipping/', views.checkout_shipping, name='checkout_shipping'),
    path('payment/', views.checkout_payment, name='checkout_payment'),
    path('confirmation/', views.checkout_confirmation, name='checkout_confirmation'),
    path('complete/', views.order_complete, name='order_complete'),
    path('api/detail/<int:order_id>/', views.order_detail_api, name='order_detail_api'),
    path('api/detail/delete/<int:order_id>/', views.delete_order, name='order_detail_api_delete'),

]