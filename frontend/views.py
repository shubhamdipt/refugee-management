from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, reverse

from locations.models import City
from organization.models import Helper
from refugee.models import Refugee


def home(request):
    """View for the home page."""
    ctx = {}
    ctx["cities"] = City.objects.order_by("name")
    return render(request, "frontend/home.html", ctx)


@login_required
def services(request):
    if Helper.objects.filter(account_user=request.user).first():
        return redirect(reverse("organization:services"))
    elif Refugee.objects.filter(account_user=request.user).first():
        return redirect(reverse("refugee:services"))
    return HttpResponseForbidden("Profile could not be found. It could be that the profile is still not verified.")


def data_privacy(request):
    """View for the data privacy page."""
    ctx = {}
    return render(request, "frontend/data_privacy.html", ctx)
