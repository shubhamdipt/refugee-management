from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


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
