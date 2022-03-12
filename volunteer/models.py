from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from locations.models import City, Route
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


class VolunteerRoute(models.Model):
    route = models.ForeignKey(Route, verbose_name=_("Route"), on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, verbose_name=_("Volunteer"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Volunteer Route")
        verbose_name_plural = _("Volunteers Routes")

    def __str__(self):
        return f"Route: {self.route.id}, Volunteer: {self.volunteer}"


class Transfer(CreateUpdateModel):
    CAR = 1
    BUS = 2
    VEHICLE_CHOICES = ((CAR, _("Car")), (BUS, _("Bus")))

    volunteer_route = models.ForeignKey(
        VolunteerRoute, verbose_name=_("Volunteer-Route"), on_delete=models.SET_NULL, null=True, blank=True
    )
    start_time = models.DateTimeField(_("Start time"), null=True, blank=True)
    total_seats = models.IntegerField(_("Total seats"), validators=[MinValueValidator(1), MaxValueValidator(1000)])
    vehicle = models.IntegerField(_("Vehicle type"), choices=VEHICLE_CHOICES, null=True, blank=True)
    vehicle_registration_number = models.CharField(
        _("Vehicle registration number"), max_length=60, null=True, blank=True
    )
    active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Transfer")
        verbose_name_plural = _("Transfers")

    def __str__(self):
        return f"{self.id}"

    @property
    def stopovers(self):
        return TransferRouteDetails.objects.filter(transfer=self).select_related("city").order_by("departure_time")

    @property
    def stopovers_text(self):
        return " -> ".join([i.city.name for i in self.stopovers])

    @property
    def route_text(self):
        cities = [str(i.city) for i in self.stopovers]
        return f"{cities[0]} -> {cities[-1]}"

    def as_dict(self, show_details=False):
        dict_obj = {
            "id": self.pk,
            "start_time": self.start_time.strftime("%d/%m/%Y %H:%M"),
            "seats": self.total_seats,
            "route": self.stopovers_text,
            "active": self.active,
            "vehicle": self.get_vehicle_display(),
            "vehicle_registration_number": self.vehicle_registration_number,
        }
        if not show_details:
            del dict_obj["vehicle"]
            del dict_obj["vehicle_registration_number"]
        return dict_obj


class TransferRouteDetails(models.Model):
    transfer = models.ForeignKey(Transfer, verbose_name=_("Transfer"), on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE)
    address = models.CharField(_("Address"), max_length=255)
    departure_time = models.DateTimeField(_("Departure time"))

    class Meta:
        verbose_name = _("Transfer Route Details")
        verbose_name_plural = _("Transfer Route Details")
        unique_together = ("transfer", "city")

    def __str__(self):
        return f"{self.transfer}: {self.id}"
