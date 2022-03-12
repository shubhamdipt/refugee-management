from django.contrib import admin

from volunteer.models import Transfer, TransferRouteDetails, Volunteer, VolunteerRoute


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("id", "account_user")
    search_fields = ("account_user__email",)


@admin.register(VolunteerRoute)
class VolunteerRouteAdmin(admin.ModelAdmin):
    list_display = ("id", "volunteer", "route")


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "volunteer_route",
        "start_time",
        "total_seats",
        "active",
        "vehicle",
        "vehicle_registration_number",
    )
    list_filter = ("start_time", "active")
    search_fields = ("volunteer_route__volunteer__email",)


@admin.register(TransferRouteDetails)
class TransferRouteDetailsAdmin(admin.ModelAdmin):
    list_display = ("id", "transfer", "city", "address", "departure_time")
