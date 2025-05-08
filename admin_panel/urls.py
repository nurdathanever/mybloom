from django.urls import path
from .views import admin_dashboard, update_order_status, admin_users, admin_products

urlpatterns = [
    path("", admin_dashboard, name="admin_dashboard"),
    path("update-order-status/<int:order_id>/", update_order_status, name="update_order_status"),
    path("users/", admin_users, name="admin_users"),
    path("products/", admin_products, name="admin_products"),
    path("orders/", admin_dashboard, name="admin_orders"),
]