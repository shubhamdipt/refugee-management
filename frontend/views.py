from django.shortcuts import render


def home(request):
    """View for the home page."""
    ctx = {}
    return render(request, "frontend/home.html", ctx)


def data_privacy(request):
    """View for the data privacy page."""
    ctx = {}
    return render(request, "frontend/data_privacy.html", ctx)
