from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
)
from django.urls import path, reverse_lazy
from django.utils.translation import gettext_lazy as _

from accounts.forms import OrganizationHelperCreationForm, RefugeeCreationForm
from accounts.views import AccountEdit, ActivateAccount, PasswordReset, RegisterAccount

app_name = "accounts"
urlpatterns = [
    path("activate/<uidb64>/<token>", ActivateAccount.as_view(), name="activate"),
    path("login", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout", LogoutView.as_view(next_page=reverse_lazy("accounts:login")), name="logout"),
    path("profile", AccountEdit.as_view(), name="profile"),
    path(
        "password-reset",
        PasswordReset.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done",
        PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "set-new-password/<uidb64>/<token>",
        PasswordResetConfirmView.as_view(
            template_name="accounts/password_new.html", success_url=reverse_lazy("accounts:password_reset_complete")
        ),
        name="set_new_password",
    ),
    path(
        "password_reset/complete",
        PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path(
        "register/refugee",
        RegisterAccount.as_view(form=RefugeeCreationForm, registration_type=_("Refugee")),
        name="register_refugee",
    ),
    path(
        "register/organization-helper",
        RegisterAccount.as_view(form=OrganizationHelperCreationForm, registration_type=_("Volunteer")),
        name="register_organization_helper",
    ),
]
