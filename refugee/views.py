from django.shortcuts import render

from refugee_management.custom_access import refugee_access


@refugee_access
def profile(request, refugee):
    return render(request, "refugee/profile.html", {})
