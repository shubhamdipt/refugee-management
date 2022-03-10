from django.shortcuts import render

from refugee.forms import TransferServiceReservationForm
from refugee.models import TransferServiceReservation
from refugee_management.custom_access import refugee_access


@refugee_access()
def services(request, refugee):
    return render(request, "refugee/services.html", {})


@refugee_access(redirect_url="/login")
def reserve_transfer_service(request, refugee, transfer_id):
    form = TransferServiceReservationForm(transfer_id=transfer_id)
    if request.method == "POST":
        form = TransferServiceReservationForm(transfer_id=transfer_id, data=request.POST)
        if form.is_valid():
            TransferServiceReservation.objects.create(
                transfer_id=transfer_id,
                refugee=refugee,
                start_city_id=form.cleaned_data["start_city"],
                end_city_id=form.cleaned_data["end_city"],
                seats=form.cleaned_data["seats"],
            )
    return render(request, "refugee/transfer_reservation.html", {"form": form})
