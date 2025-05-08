from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="account_login"),
    path("signup/", signup_view, name="account_signup"),
    path("profile/", profile_view, name="profile"),
    path("change-password/", change_password, name="change_password"),
    path('profile/payment/', payment_method_view, name='payment_method'),
    path('profile/history/', order_history_view, name='order_history'),
    path('profile/history/ajax', order_history_ajax_view, name='order_history_ajax'),
    path('profile/bonuses/', my_bonuses_view, name='bonuses'),
]