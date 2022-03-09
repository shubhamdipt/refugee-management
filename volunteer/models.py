from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


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
