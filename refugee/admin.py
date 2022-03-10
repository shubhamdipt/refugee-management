from django.contrib import admin

from refugee.models import Refugee, TransferServiceReservation


@admin.register(Refugee)
class RefugeeAdmin(admin.ModelAdmin):
    list_display = ("id", "account_user")
    search_fields = ("account_user__email",)


@admin.register(TransferServiceReservation)
class TransferServiceReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "refugee", "transfer", "start_city", "end_city")
    search_fields = ("refugee__account_user__email",)
    ordering = ("-transfer__pick_up_time",)
