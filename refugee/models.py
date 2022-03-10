from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from locations.models import City
from refugee_management.models import CreateUpdateModel
from volunteer.models import TransferService


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
    transfer = models.ForeignKey(TransferService, verbose_name=_("Transfer"), on_delete=models.CASCADE)
    refugee = models.ForeignKey(Refugee, verbose_name=_("Refugee"), on_delete=models.CASCADE)
    start_city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE, related_name="start_city")
    end_city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE, related_name="end_city")
    seats = models.IntegerField(_("Seats"), validators=[MinValueValidator(1), MaxValueValidator(1000)])

    class Meta:
        verbose_name = _("Transfer Service Reservation")
        verbose_name_plural = _("Transfer Service Reservations")
        unique_together = ("transfer", "refugee")

    def __str__(self):
        return f"{self.refugee} -> {self.transfer}"
