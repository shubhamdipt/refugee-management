from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from accounts.models import AccountUser
from accounts.tokens import account_activation_token, password_reset_token


def send_activation_email(user: AccountUser, request):
    current_site = get_current_site(request)
    message = render_to_string(
        "emails/account_activation.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    msg = EmailMessage(
        subject=_("Account activation"),
        body=message,
        to=[user.email],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()


def send_password_reset_email(user: AccountUser, request):
    current_site = get_current_site(request)
    message = render_to_string(
        "emails/password_reset.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": password_reset_token.make_token(user),
        },
    )
    msg = EmailMessage(
        subject=_("Password Reset requested"),
        body=message,
        to=[user.email],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
