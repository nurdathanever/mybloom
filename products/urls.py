from django.urls import path
from .views import product_list, product_detail, product_create, product_delete, product_update

urlpatterns = [
    path("", product_list, name="product_list"),
    path("create/", product_create, name="product_create"),
    path("<int:pk>/edit/", product_update, name="product_update"),
    path("<int:pk>/delete/", product_delete, name="product_delete"),
    path("<int:product_id>/", product_detail, name="product_detail"),
]