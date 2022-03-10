from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from locations.models import Route, RouteCities
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
class Transfer(CreateUpdateModel):
    volunteer = models.ForeignKey(
        Volunteer, verbose_name=_("Volunteer"), on_delete=models.SET_NULL, null=True, blank=True
    )
    route = models.ForeignKey(Route, verbose_name=_("Route"), on_delete=models.SET_NULL, null=True, blank=True)
    pick_up_time = models.DateTimeField(_("Pick up time"))
    total_seats = models.IntegerField("Total seats", validators=[MinValueValidator(1), MaxValueValidator(1000)])
    active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Transfer Service")
        verbose_name_plural = _("Transfer Service")

    def __str__(self):
        return f"{self.pick_up_time}: {self.volunteer}"

    @property
    def stopovers(self):
        return RouteCities.objects.filter(route=self.route).select_related("city").order_by("route_order")

    @property
    def stopovers_text(self):
        return " -> ".join([i.city.name for i in self.stopovers])

    @property
    def route_text(self):
        cities = [str(i.city) for i in self.stopovers]
        return f"{cities[0]} -> {cities[-1]}"

    def as_dict(self):
        return {
            "id": self.pk,
            "pick_up_time": self.pick_up_time.strftime("%d/%m/%Y %H:%M"),
            "total_seats": self.total_seats,
            "route": self.stopovers_text,
        }
