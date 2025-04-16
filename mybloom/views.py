from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

def create_admin_user(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@gmail.com",
            password="mybloomadmin"
        )
        return HttpResponse("Admin created.")
    return HttpResponse("Admin already exists.")

def home(request):
    return render(request, "home.html")

def catalog(request):
    return render(request, "catalog.html")