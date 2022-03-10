from django.contrib import admin

from volunteer.models import Transfer, Volunteer


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account_user",
    )
    search_fields = ("account_user__email",)


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "pick_up_time", "total_seats", "active")
    list_filter = ("pick_up_time", "active")
