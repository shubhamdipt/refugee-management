from datetime import datetime

from django.shortcuts import redirect, render, reverse
from django.views.decorators.http import require_POST

from refugee_management.custom_access import volunteer_access


@volunteer_access
def services(request, volunteer):
    return render(request, "volunteer/services.html", {})


@volunteer_access
@require_POST
def add_transfer_service(request, volunteer):
    transfer_datetime = datetime.strptime(request.POST.get("transfer-datetime"), "%d/%m/%Y %H:%M")
    transfer_refugees = request.POST.get("transfer-refugees")
    cities = []
    count = 1
    while True:
        key = f"transfer-stop-{count}"
        city_id = request.POST.get(key)
        if city_id:
            pass
    return redirect(reverse("volunteer:services"))
