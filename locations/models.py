from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import IntegrityError, models
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


class RouteManager(models.Manager):
    def get_or_create_with_cities_ids(self, cities_ids: list):
        if len(set(cities_ids)) != len(cities_ids):
            raise IntegrityError
        cities_combination = "-".join(cities_ids)
        obj, created = self.get_queryset().get_or_create(cities_combination=cities_combination)
        if created:
            for count, value in enumerate(cities_ids):
                RouteCities.objects.create(route=obj, city=City.objects.get(id=value), route_order=(count + 1))
        return obj, created


class Route(models.Model):
    cities_combination = models.CharField(_("Cities combination"), max_length=255, unique=True)

    objects = RouteManager()

    class Meta:
        verbose_name = _("Route")
        verbose_name_plural = _("Routes")

    def __str__(self):
        return f"{self.pk}"


class RouteCities(models.Model):
    route = models.ForeignKey(Route, verbose_name=_("Route"), on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE)
    route_order = models.IntegerField("Order", validators=[MinValueValidator(1), MaxValueValidator(100)])

    class Meta:
        verbose_name = _("Route Cities")
        verbose_name_plural = _("Route Cities")
        unique_together = (("route", "city"), ("route", "route_order"))

    def __str__(self):
        return f"{self.route}: {self.city} ({self.route_order})"
