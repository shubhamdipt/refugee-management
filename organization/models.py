from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from locations.models import City, Route
from refugee_management.models import CreateUpdateModel

TIMEZONE = settings.TIME_ZONE


class Organization(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    address = models.CharField(_("Address"), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self):
        return self.name


class Helper(models.Model):
    ADMIN = 1
    HELPER = 2

    ACCOUNT_TYPES = ((ADMIN, _("Admin")), (HELPER, _("Helper")))

    organization = models.ForeignKey(
        Organization,
        verbose_name=_("Organization"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    account_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    account_type = models.IntegerField(_("Account type"), choices=ACCOUNT_TYPES)
    verified = models.BooleanField(_("Verified"), default=False)

    class Meta:
        verbose_name = _("Helper")
        verbose_name_plural = _("Helpers")

    def __str__(self):
        first_name = self.account_user.first_name
        last_name = self.account_user.last_name
        email = self.account_user.email
        return f"{first_name if first_name else ''} {last_name if last_name else ''} - {email}"

    def as_dict(self):
        return {
            "id": self.id,
            "organization": self.organization.name,
            "first_name": self.account_user.first_name,
            "last_name": self.account_user.last_name,
            "email": self.account_user.email,
            "phone": self.account_user.phone,
            "account_type": self.get_account_type_display(),
            "verified": self.verified,
        }


class OrganizationRules(models.Model):
    headline = models.CharField(_("Headline"), unique=True, max_length=63)
    rules = models.TextField(_("Rules"))
    organization = models.ForeignKey(
        Organization,
        verbose_name=_("Organization"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Organization Rules")
        verbose_name_plural = _("Organizations Rules")

    def __str__(self):
        return f"{self.headline}: {self.organization.name}"


class OrganizationPickUpPoint(models.Model):
    organization = models.ForeignKey(
        Organization,
        verbose_name=_("Organization"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE)
    address = models.CharField(_("Address"), max_length=255)

    class Meta:
        verbose_name = _("Organization Pick Up point")
        verbose_name_plural = _("Organization Pick Up points")
        unique_together = ("city", "address")

    def __str__(self):
        return f"{self.city}: {self.address}"


class OrganizationRoute(models.Model):
    """This model connects an organization with possible routes for search purposes."""

    route = models.ForeignKey(
        Route,
        verbose_name=_("Route"),
        on_delete=models.CASCADE,
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name=_("Organization"),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Organization Route")
        verbose_name_plural = _("Organization Routes")

    def __str__(self):
        return f"Route: {self.route.id}, Organization: {self.organization}"


class Transfer(CreateUpdateModel):
    CAR = 1
    BUS = 2
    VEHICLE_CHOICES = ((CAR, _("Car")), (BUS, _("Bus")))

    organization_route = models.ForeignKey(
        OrganizationRoute,
        verbose_name=_("Organization route"),
        on_delete=models.CASCADE,
    )
    helper = models.ForeignKey(
        Helper,
        verbose_name=_("Helper"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_helper",
    )
    secondary_helper = models.ForeignKey(
        Helper,
        verbose_name=_("Secondary Helper"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="secondary_helper",
    )
    start_time = models.DateTimeField(_("Start time"), null=True, blank=True)
    refugee_seats = models.IntegerField(
        _("Refugee seats"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
    )
    helper_seats = models.IntegerField(
        _("Helper seats"),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
    )
    driver_seats = models.IntegerField(
        _("Driver seats"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
    )
    vehicle = models.IntegerField(_("Vehicle type"), choices=VEHICLE_CHOICES, null=True, blank=True)
    vehicle_registration_number = models.CharField(
        _("Vehicle registration number"), max_length=60, null=True, blank=True
    )
    food = models.BooleanField(_("Food "), default=False)
    drinks = models.BooleanField(_("Drinks"), default=False)
    blanket = models.BooleanField(_("Blanket"), default=False)
    healthcare = models.BooleanField(_("Healthcare personnel"), default=False)
    translators = models.CharField(_("Translators"), max_length=255, null=True, blank=True)
    description = models.TextField(_("Additional remarks"), null=True, blank=True)
    rules = models.ForeignKey(
        OrganizationRules,
        verbose_name=_("Rules"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
            "organization": self.organization_route.organization.name,
            "helper": self.helper.account_user.email if self.helper else None,
            "secondary_helper": self.secondary_helper.email if self.secondary_helper else None,
            "start_time": timezone.localtime(self.start_time).strftime("%d/%m/%Y %H:%M") if self.start_time else None,
            "refugee_seats": self.refugee_seats,
            "food": self.food,
            "drinks": self.drinks,
            "healthcare": self.healthcare,
            "description": self.description,
            "route": self.stopovers_text,
            "active": self.active,
        }
        if show_details:
            dict_obj["helper_seats"] = self.helper_seats
            dict_obj["driver_seats"] = self.driver_seats
            dict_obj["vehicle"] = self.get_vehicle_display() if self.vehicle else None
            dict_obj["vehicle_registration_number"] = self.vehicle_registration_number
        return dict_obj


class TransferRouteDetails(models.Model):
    transfer = models.ForeignKey(
        Transfer,
        verbose_name=_("Transfer"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    city = models.ForeignKey(
        City,
        verbose_name=_("City"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="org_transfer_city",
    )
    address = models.CharField(_("Address"), max_length=255, null=True, blank=True)
    departure_time = models.DateTimeField(_("Departure time"))

    class Meta:
        verbose_name = _("Transfer Route Details")
        verbose_name_plural = _("Transfer Route Details")

    def __str__(self):
        return f"{self.transfer}: {self.city} at {self.departure_time}"

    def as_dict(self):
        return {
            "id": self.id,
            "city": self.city.name,
            "address": self.address,
            "departure_time": timezone.localtime(self.departure_time).strftime("%d/%m/%Y %H:%M")
            if self.departure_time
            else None,
        }
