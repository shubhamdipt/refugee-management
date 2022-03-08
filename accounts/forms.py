from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from accounts.models import AccountUser


class AccountUserCreationForm(UserCreationForm):
    class Meta:
        model = AccountUser
        fields = ("email", "password")


class AccountUserChangeForm(UserChangeForm):
    class Meta:
        model = AccountUser
        fields = ("email", "password")
