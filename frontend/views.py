from django.shortcuts import render

from accounts.forms import AccountUserCreationForm


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
    return render(request, "frontend/home.html", ctx)


def data_privacy(request):
    """View for the data privacy page."""
    ctx = {}
    return render(request, "frontend/data_privacy.html", ctx)
