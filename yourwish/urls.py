from django.urls import path
from . import views

urlpatterns = [
    path("", views.yourwish_tabs, name="yourwish_tabs"),
    path("bloom/", views.yourwish_bloomit, name="yourwish_bloomit"),
    path("confirm/", views.yourwish_confirm_bouquet, name="yourwish_confirm_bouquet"),
]