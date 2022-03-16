import itertools

from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy

from organization.models import Transfer, TransferRouteDetails
from organization.seats_management import SeatsManagement
from refugee.forms import TransferReservationForm
from refugee.models import TransferReservation
from refugee_management.custom_access import refugee_access


@refugee_access()
def services(request, refugee):
    return render(request, "refugee/services.html", {})


@refugee_access(redirect_url=reverse_lazy("accounts:login"))
def reserve_transfer(request, refugee, transfer_id):
    transfer = Transfer.objects.get(id=transfer_id)

    # Creating seat availabilities
    availabilities = []
    seats_management = SeatsManagement(transfer=transfer)
    available_seats = seats_management.determine_available_seats(return_by_name=True)
    city_combinations = list(itertools.combinations([str(i.city) for i in transfer.stopovers], 2))
    for from_city, to_city in city_combinations:
        availabilities.append((from_city, to_city, available_seats.get((from_city, to_city))))
    route_details = [(i["departure_time"], i["city"], i["address"]) for i in seats_management.route_details]
    transfer_properties = transfer.as_dict()

    form = TransferReservationForm(transfer=transfer, refugee=refugee)
    if request.method == "POST":
        form = TransferReservationForm(transfer=transfer, refugee=refugee, data=request.POST)
        if form.is_valid():
            from_city = TransferRouteDetails.objects.get(city_id=form.cleaned_data["from_city"], transfer=transfer)
            to_city = TransferRouteDetails.objects.get(city_id=form.cleaned_data["to_city"], transfer=transfer)
            TransferReservation.objects.create(
                transfer=transfer,
                refugee=refugee,
                from_city=from_city,
                to_city=to_city,
                seats=form.cleaned_data["seats"],
            )
            return redirect(reverse("refugee:services"))
    return render(
        request,
        "refugee/transfer_reservation.html",
        {
            "form": form,
            "transfer": transfer,
            "seats": availabilities,
            "route": route_details,
            "transfer_properties": transfer_properties,
        },
    )


@refugee_access()
def delete_transfer_reservation(request, refugee, reservation_id):
    TransferReservation.objects.filter(id=reservation_id, refugee=refugee).delete()
    return redirect(reverse("refugee:services"))


@refugee_access()
def transfer_reservation_details(request, refugee, reservation_id):
    return render(request, "refugee/transfer_reservation_details.html", {"reservation_id": reservation_id})
