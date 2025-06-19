from django.urls import path
from .views import admin_dashboard, update_order_status, admin_users, admin_products, update_product, delete_product

urlpatterns = [
    path("", admin_dashboard, name="admin_dashboard"),
    path("update-order-status/<int:order_id>/", update_order_status, name="update_order_status"),
    path("users/", admin_users, name="admin_users"),
    path("products/", admin_products, name="admin_products"),
    path("orders/", admin_dashboard, name="admin_orders"),
    path("products/update/<int:product_id>/", update_product, name="update_product"),
    path("products/delete/<int:product_id>/", delete_product, name="delete_product"),
]