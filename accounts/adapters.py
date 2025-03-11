from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url
import logging

logger = logging.getLogger(__name__)

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user

        if not user.is_authenticated:
            return resolve_url("account_login")  # Ensure redirect is never None

        if user.role == "admin":
            return resolve_url("admin_dashboard")  # Redirect admins to dashboard

        return resolve_url("home")  # Redirect regular users to home