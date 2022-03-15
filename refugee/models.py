from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from organization.models import Transfer, TransferRouteDetails
from refugee_management.models import CreateUpdateModel


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


class TransferReservation(CreateUpdateModel):
    transfer = models.ForeignKey(Transfer, verbose_name=_("Transfer"), on_delete=models.CASCADE)
    refugee = models.ForeignKey(Refugee, verbose_name=_("Refugee"), on_delete=models.CASCADE)
    from_city = models.ForeignKey(
        TransferRouteDetails, verbose_name=_("From city"), on_delete=models.CASCADE, related_name="start_city"
    )
    to_city = models.ForeignKey(
        TransferRouteDetails, verbose_name=_("To city"), on_delete=models.CASCADE, related_name="end_city"
    )
    seats = models.IntegerField(_("Seats"), validators=[MinValueValidator(1), MaxValueValidator(1000)])

    class Meta:
        verbose_name = _("Transfer Reservation")
        verbose_name_plural = _("Transfer Reservations")
        unique_together = ("transfer", "refugee")

    def __str__(self):
        return f"{self.refugee} -> {self.transfer}"

    @property
    def route_text(self):
        route_cities = []
        start = False
        for route_city in self.transfer.stopovers:
            if route_city.city == self.from_city.city:
                start = True
            if start:
                route_cities.append(route_city.city.name)
            if route_city.city == self.to_city.city:
                break
        return " -> ".join(route_cities)

    def as_dict(self):
        return {
            "id": self.id,
            "route": self.route_text,
            "seats": self.seats,
            "departure_time": self.from_city.departure_time.strftime("%d/%m/%Y %H:%M"),
        }
