from django.contrib import admin
from .models import User, Bonus
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("role", "phone", "city", "street", "building", "apartment", "photo")}),  # ✅ Ensure role is included
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("role", "phone","city", "street", "building", "apartment", "photo")}),
    )
    list_display = UserAdmin.list_display + ("phone", "city", "street", "building", "apartment", "photo")
    list_filter = ("role", "is_staff", "is_active")  # ✅ Enable filtering by role
    search_fields = ("username", "email", "role")

admin.site.register(User, CustomUserAdmin)
admin.site.register(Bonus)