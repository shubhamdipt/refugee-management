from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, reverse
from django.utils import timezone

from accounts.forms import AccountUserCreationForm
from refugee.models import Refugee
from volunteer.models import TransferService, Volunteer


def home(request):
    """View for the home page."""
    ctx = {}
    form = AccountUserCreationForm()
    if request.method == "POST":
        form = AccountUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            ctx["success"] = "Successfully registered. Please login."
            form = AccountUserCreationForm()
    ctx["registration_form"] = form
    ctx["transfers"] = TransferService.objects.filter(pick_up_time__gte=timezone.now()).order_by("-pick_up_time")
    return render(request, "frontend/home.html", ctx)


@login_required
def services(request):
    if Volunteer.objects.filter(account_user=request.user).first():
        return redirect(reverse("volunteer:services"))
    elif Refugee.objects.filter(account_user=request.user).first():
        return redirect(reverse("refugee:services"))
    return HttpResponseForbidden("Profile could not be found.")


def data_privacy(request):
    """View for the data privacy page."""
    ctx = {}
    return render(request, "frontend/data_privacy.html", ctx)
