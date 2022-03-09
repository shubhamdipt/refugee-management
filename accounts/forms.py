from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from accounts.models import AccountUser
from refugee.models import Refugee
from volunteer.models import Volunteer


class AccountUserCreationForm(UserCreationForm):
    REFUGEE = "refugee"
    VOLUNTEER = "volunteer"

    account_type = forms.ChoiceField(
        label=_("Account type"), choices=((REFUGEE, _("Refugee")), (VOLUNTEER, _("Volunteer")))
    )

    class Meta:
        model = AccountUser
        fields = ("account_type", "email", "password1", "password2")

    def save(self, commit=True):
        account_user = super().save(commit=commit)
        if commit:
            if self.cleaned_data["account_type"] == self.VOLUNTEER:
                Volunteer.objects.get_or_create(account_user=account_user)
            elif self.cleaned_data["account_type"] == self.REFUGEE:
                Refugee.objects.get_or_create(account_user=account_user)
        return account_user
