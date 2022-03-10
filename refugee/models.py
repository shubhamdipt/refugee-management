from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from locations.models import City
from refugee_management.models import CreateUpdateModel
from volunteer.models import Transfer


class Refugee(models.Model):
    account_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Refugee")
        verbose_name_plural = _("Refugees")

    def __str__(self):
        return self.account_user.email


class TransferServiceReservation(CreateUpdateModel):
    transfer = models.ForeignKey(Transfer, verbose_name=_("Transfer"), on_delete=models.CASCADE)
    refugee = models.ForeignKey(Refugee, verbose_name=_("Refugee"), on_delete=models.CASCADE)
    start_city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE, related_name="start_city")
    end_city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE, related_name="end_city")
    seats = models.IntegerField(_("Seats"), validators=[MinValueValidator(1), MaxValueValidator(1000)])

    class Meta:
        verbose_name = _("Transfer Reservation")
        verbose_name_plural = _("Transfer Reservations")
        unique_together = ("transfer", "refugee")

    def __str__(self):
        return f"{self.refugee} -> {self.transfer}"

    def route_text(self):
        route_cities = []
        start = False
        for route_city in self.transfer.stopovers:
            if route_city.city == self.start_city:
                start = True
            if start:
                route_cities.append(route_city.city.name)
            if route_city.city == self.end_city:
                break
        return " -> ".join(route_cities)
