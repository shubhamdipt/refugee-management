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
