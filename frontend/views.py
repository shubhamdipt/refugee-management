from django.shortcuts import render


def home(request):
    """View for the home page."""
    ctx = {}
    return render(request, "frontend/home.html", ctx)
