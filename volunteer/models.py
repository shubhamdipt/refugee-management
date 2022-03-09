from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from locations.models import City
from refugee_management.models import CreateUpdateModel


class Volunteer(models.Model):
    account_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Volunteer")
        verbose_name_plural = _("Volunteers")

    def __str__(self):
        return self.account_user.email


# Services
class TransferService(CreateUpdateModel):
    volunteer = models.ForeignKey(Volunteer, verbose_name=Volunteer, on_delete=models.SET_NULL, null=True, blank=True)
    pick_up_time = models.DateTimeField(_("Pick up time"))
    total_seats = models.IntegerField("Total seats", validators=[MinValueValidator(1), MaxValueValidator(1000)])
    active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Transfer Service")
        verbose_name_plural = _("Transfer Service")

    def __str__(self):
        return f"{self.pick_up_time}: {self.volunteer}"


class TransferRouteCities(models.Model):
    transfer_id = models.ForeignKey(TransferService, verbose_name=_("Transfer ID"), on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE)
    route_order = models.IntegerField("Order", validators=[MinValueValidator(1), MaxValueValidator(100)])

    class Meta:
        verbose_name = _("Transfer Route Cities")
        verbose_name_plural = _("Transfer Route Cities")
        unique_together = ("transfer_id", "city")

    def __str__(self):
        return f"{self.transfer_id}: {self.city} ({self.route_order})"
