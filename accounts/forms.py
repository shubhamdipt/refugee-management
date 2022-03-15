from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from accounts.emails import send_activation_email
from accounts.models import AccountUser
from organization.models import Helper, Organization
from refugee.models import Refugee


class AccountUserCreationForm(UserCreationForm):
    class Meta:
        model = AccountUser
        fields = ("email", "password1", "password2")

    def save(self, commit=False, request=None):
        account_user = super().save(commit=commit)
        account_user.is_active = False
        account_user.save()
        send_activation_email(user=account_user, request=request)
        self._create_user_by_account_type(user=account_user)
        return account_user

    def _create_user_by_account_type(self, user: AccountUser):
        raise NotImplementedError


class RefugeeCreationForm(AccountUserCreationForm):
    class Meta:
        model = AccountUser
        fields = ("email", "password1", "password2")

    def _create_user_by_account_type(self, user: AccountUser):
        Refugee.objects.get_or_create(account_user=user)


class OrganizationHelperCreationForm(AccountUserCreationForm):
    organization = forms.ChoiceField(label=_("Organization"))

    class Meta:
        model = AccountUser
        fields = ("organization", "first_name", "last_name", "email", "phone", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["organization"].choices = ((i.id, i.name) for i in Organization.objects.order_by("name"))

    def _create_user_by_account_type(self, user: AccountUser):
        Helper.objects.get_or_create(
            account_user=user, organization_id=self.cleaned_data["organization"], account_type=Helper.HELPER
        )


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = AccountUser
        fields = ("first_name", "last_name")
