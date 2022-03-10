from django.contrib import admin

from volunteer.models import TransferRouteCities, TransferService, Volunteer


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("account_user",)
    search_fields = ("account_user__email",)


@admin.register(TransferService)
class TransferServiceAdmin(admin.ModelAdmin):
    list_display = ("created", "pick_up_time", "total_seats", "active")
    list_filter = ("pick_up_time", "active")


@admin.register(TransferRouteCities)
class TransferRouteCitiesAdmin(admin.ModelAdmin):
    list_display = ("transfer", "city", "route_order")
