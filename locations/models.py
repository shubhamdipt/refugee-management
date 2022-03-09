import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, verbose_name=_("Country"), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=255)

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        unique_together = ("name", "country")

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class Route(models.Model):
    route_id = models.UUIDField(_("Route ID"), default=uuid.uuid4, editable=False)
    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE)
    route_order = models.IntegerField("Order", validators=[MinValueValidator(1), MaxValueValidator(100)])

    class Meta:
        verbose_name = _("Route")
        verbose_name_plural = _("Routes")
        unique_together = ("route_id", "city")

    def __str__(self):
        return f"{self.route_id}: {self.city} ({self.route_order})"
