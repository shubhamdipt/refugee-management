from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import AccountUser


@admin.register(AccountUser)
class AccountUserAdmin(UserAdmin):
    list_display = (
        "email",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2", "is_staff", "is_active")}),
    )
    search_fields = ("email",)
    ordering = ("email",)
