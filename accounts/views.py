from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View

from accounts.emails import send_password_reset_email
from accounts.forms import AccountEditForm
from accounts.tokens import account_activation_token

User = get_user_model()


class RegisterAccount(View):
    form = None
    template = "accounts/register.html"
    registration_type = None

    def get(self, request):
        ctx = {}
        form = self.form()
        ctx["registration_form"] = form
        ctx["registration_type"] = self.registration_type
        return render(request, self.template, ctx)

    def post(self, request):
        ctx = {}
        form = self.form(request.POST)
        if form.is_valid():
            form.save(request=request)
            ctx["success"] = "A verification email has been sent. Please check your inbox."
            form = self.form()
        ctx["registration_form"] = form
        ctx["registration_type"] = self.registration_type
        return render(request, self.template, ctx)


class PasswordReset(View):
    form = PasswordResetForm
    template = "accounts/password_reset.html"
    email_template = ("emails/password_reset.html",)
    success_url = reverse_lazy("accounts:password_reset_done")

    def get(self, request):
        return render(request, self.template, {"form": self.form()})

    def post(self, request):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data["email"]
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    send_password_reset_email(user=user, request=request)
                    return redirect(reverse_lazy("accounts:password_reset_done"))


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("frontend:home")
        else:
            messages.warning(
                request, ("The confirmation link was invalid, possibly because it has already been used.")
            )
            return redirect("home")


@method_decorator(login_required, name="dispatch")
class AccountEdit(View):
    form = AccountEditForm
    template = "accounts/profile.html"
    registration_type = None

    def get(self, request):
        form = self.form(instance=request.user)
        return render(request, self.template, {"user": request.user, "form": form})

    def post(self, request):
        ctx = {"user": request.user}
        form = self.form(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            ctx["success"] = "The form has been successfully submitted."
        ctx["form"] = form
        return render(request, self.template, ctx)
