from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import login, get_user_model, logout, update_session_auth_hash
from .forms import CustomUserCreationForm, ProfileUpdateForm, CustomPasswordChangeForm
from django.contrib import messages
from allauth.account.views import LoginView


User = get_user_model()

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = "django.contrib.auth.backends.ModelBackend"
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile_view(request):
    """Display and edit user profile."""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})


@login_required
def change_password(request):
    """Allow user to change password."""
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect("profile")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "accounts/change_password.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    """Custom login view to redirect users based on their role after login."""
    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == "admin":
                return resolve_url("admin_dashboard")  # Admins → admin dashboard
        return resolve_url("home")  # Users → main page

    def get_template_names(self):
        # Print the template path being used
        print(f"Template used: {self.template_name}")
        return [self.template_name]

    def dispatch(self, request, *args, **kwargs):
        print("CustomLoginView is being called!")  # Debug log
        return super().dispatch(request, *args, **kwargs)