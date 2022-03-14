from django.contrib import admin

from organization.models import (
    Helper,
    Organization,
    OrganizationPickUpPoint,
    OrganizationRoute,
    Transfer,
    TransferRouteDetails,
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address")


@admin.register(Helper)
class HelperAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "account_user", "account_type", "verified")
    list_filter = ("account_type", "verified")
    search_fields = ("account_user__email", "organization__name")


@admin.register(OrganizationPickUpPoint)
class OrganizationPickUpPointAdmin(admin.ModelAdmin):
    list_display = ("organization", "city", "address")
    list_filter = ("organization", "city")


@admin.register(OrganizationRoute)
class OrganizationRouteRouteAdmin(admin.ModelAdmin):
    list_display = ("id", "organization", "route")


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "organization_route",
        "helper",
        "start_time",
        "refugee_seats",
        "active",
        "vehicle",
        "vehicle_registration_number",
    )
    list_filter = ("start_time", "active", "organization_route")
    search_fields = ("helper__email",)


@admin.register(TransferRouteDetails)
class TransferRouteDetailsAdmin(admin.ModelAdmin):
    list_display = ("id", "transfer", "city", "address", "departure_time")
