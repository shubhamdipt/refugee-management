from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from locations.models import Route
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
    route = models.ForeignKey(Route, verbose_name=_("Route"), on_delete=models.CASCADE)
    total_seats = models.IntegerField("Total seats", validators=[MinValueValidator(1), MaxValueValidator(1000)])
    active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Transfer Service")
        verbose_name_plural = _("Transfer Service")

    def __str__(self):
        return f"{self.pick_up_time}: {self.route} ({self.volunteer})"
