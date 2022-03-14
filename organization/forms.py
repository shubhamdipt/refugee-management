from django import forms

from organization.models import OrganizationPickUpPoint


class PickUpPointForm(forms.ModelForm):
    class Meta:
        model = OrganizationPickUpPoint
        fields = ("city", "address")
