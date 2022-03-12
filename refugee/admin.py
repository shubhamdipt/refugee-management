from django.contrib import admin

from refugee.models import Refugee, TransferReservation


@admin.register(Refugee)
class RefugeeAdmin(admin.ModelAdmin):
    list_display = ("id", "account_user")
    search_fields = ("account_user__email",)


@admin.register(TransferReservation)
class TransferReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "refugee", "transfer", "from_city", "to_city")
    search_fields = ("refugee__account_user__email",)
    ordering = ("-transfer__pick_up_time",)
