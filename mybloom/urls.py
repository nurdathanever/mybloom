from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import home, catalog

urlpatterns = [
    path("", home, name="home"),
    path("catalog/", catalog, name="catalog"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
]

