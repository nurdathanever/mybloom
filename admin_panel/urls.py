from django.urls import path
from .views import admin_dashboard, update_order_status

urlpatterns = [
    path("", admin_dashboard, name="admin_dashboard"),
    path("update-order-status/<int:order_id>/", update_order_status, name="update_order_status"),
]