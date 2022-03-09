from django.db import models


class CreateUpdateModel(models.Model):
    """
    Store timestamps for creation and last modification.
    """

    created = models.DateTimeField("Created", auto_now_add=True)
    modified = models.DateTimeField("Modified", auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = "created"
        ordering = ("created",)
