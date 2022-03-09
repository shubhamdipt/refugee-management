from django.contrib import admin

from refugee.models import Refugee


@admin.register(Refugee)
class RefugeeAdmin(admin.ModelAdmin):
    list_display = ("account_user",)
    search_fields = ("account_user__email",)
