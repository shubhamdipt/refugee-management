from datetime import datetime

from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render, reverse
from django.views.decorators.http import require_POST

from locations.models import City
from refugee_management.custom_access import volunteer_access
from volunteer.models import TransferRouteCities, TransferService


@volunteer_access
def services(request, volunteer):
    return render(
        request,
        "volunteer/services.html",
        {"transfers": TransferService.objects.filter(volunteer=volunteer).order_by("-pick_up_time")},
    )


@transaction.atomic
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
            cities.append(city_id)
            count += 1
        else:
            break
    if not (transfer_datetime and transfer_refugees and len(cities) > 1):
        return HttpResponseBadRequest("Invalid form submitted.")
    try:
        obj, created = TransferService.objects.get_or_create(
            volunteer=volunteer,
            total_seats=int(transfer_refugees),
            pick_up_time=transfer_datetime,
        )
        if created:
            for count, value in enumerate(cities):
                TransferRouteCities.objects.create(
                    transfer=obj, city=City.objects.get(id=value), route_order=(count + 1)
                )
    except IntegrityError as e:
        return HttpResponseBadRequest("Invalid form submitted. Same cities have been entered more once as stopovers.")
    return redirect(reverse("volunteer:services"))


@volunteer_access
def delete_transfer_service(request, volunteer, transfer_id):
    TransferService.objects.filter(id=transfer_id, volunteer=volunteer).delete()
    return redirect(reverse("volunteer:services"))
