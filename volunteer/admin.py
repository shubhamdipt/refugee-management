from django.contrib import admin

from volunteer.models import TransferRouteCities, Volunteer


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("account_user",)
    search_fields = ("account_user__email",)


@admin.register(TransferRouteCities)
class TransferRouteCitiesAdmin(admin.ModelAdmin):
    list_display = ("transfer_id", "city", "route_order")
