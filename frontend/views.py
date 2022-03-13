from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, reverse

from locations.models import City
from refugee.models import Refugee
from volunteer.models import Volunteer


def home(request):
    """View for the home page."""
    ctx = {}
    ctx["cities"] = City.objects.order_by("name")
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
