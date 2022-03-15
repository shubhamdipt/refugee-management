from crispy_forms.helper import FormHelper
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from organization.models import (
    Helper,
    OrganizationPickUpPoint,
    OrganizationTransferRules,
    Transfer,
)


class PickUpPointForm(forms.ModelForm):
    class Meta:
        model = OrganizationPickUpPoint
        fields = ("city", "address")

    def __init__(self, helper: Helper, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HelperForm(forms.ModelForm):
    read_only_fields = ("organization", "account_user")

    class Meta:
        model = Helper
        fields = ("organization", "account_user", "account_type", "verified")

    def __init__(self, helper: Helper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.read_only_fields:
            self.fields[field].disabled = True

    def clean(self):
        data = super().clean()
        for field in self.read_only_fields:
            data[field] = getattr(self.instance, field)
        return data


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = (
            "helper",
            "secondary_helper",
            "refugee_seats",
            "helper_seats",
            "driver_seats",
            "vehicle",
            "vehicle_registration_number",
            "food",
            "drinks",
            "blanket",
            "healthcare",
            "translators",
            "rules",
            "description",
        )

    def __init__(self, helper: Helper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        valid_helpers = Helper.objects.filter(organization=helper.organization, verified=True)
        self.fields["helper"].required = True
        self.fields["helper"].queryset = valid_helpers
        self.fields["secondary_helper"].queryset = valid_helpers
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-offset-1 col-sm-4"
        self.helper.field_class = "col-sm-7"

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("helper") == cleaned_data.get("secondary_helper"):
            raise ValidationError(_("Secondary and primary helper cannot be the same."))


class OrganizationTransferRulesForm(forms.ModelForm):
    class Meta:
        model = OrganizationTransferRules
        fields = ("headline", "rules")
