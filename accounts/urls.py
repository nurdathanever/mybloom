from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view, profile_view, change_password, CustomLoginView, logout_view

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="account_login"),
    path("logout/", logout_view, name="account_logout"),
    path("signup/", signup_view, name="account_signup"),
    path("profile/", profile_view, name="profile"),
    path("change-password/", change_password, name="change_password"),
]