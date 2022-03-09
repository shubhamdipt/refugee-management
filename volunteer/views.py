from django.shortcuts import render

from refugee_management.custom_access import volunteer_access


@volunteer_access
def profile(request, volunteer):
    return render(request, "volunteer/profile.html", {})
