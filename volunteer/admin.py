from django.contrib import admin

from volunteer.models import Volunteer


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("account_user",)
    search_fields = ("account_user__email",)
