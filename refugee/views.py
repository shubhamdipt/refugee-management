from django.shortcuts import redirect, render, reverse

from refugee.forms import TransferServiceReservationForm
from refugee.models import TransferServiceReservation
from refugee_management.custom_access import refugee_access
from volunteer.models import Transfer


@refugee_access()
def services(request, refugee):
    return render(
        request,
        "refugee/services.html",
        {
            "transfer_reservations": TransferServiceReservation.objects.filter(refugee=refugee)
            .select_related("transfer")
            .order_by("-transfer__pick_up_time")
        },
    )


@refugee_access(redirect_url="/login")
def reserve_transfer_service(request, refugee, transfer_id):
    transfer = Transfer.objects.get(id=transfer_id)
    form = TransferServiceReservationForm(transfer=transfer, refugee=refugee)
    if request.method == "POST":
        form = TransferServiceReservationForm(transfer=transfer, refugee=refugee, data=request.POST)
        if form.is_valid():
            TransferServiceReservation.objects.create(
                transfer=transfer,
                refugee=refugee,
                start_city_id=form.cleaned_data["start_city"],
                end_city_id=form.cleaned_data["end_city"],
                seats=form.cleaned_data["seats"],
            )
            return redirect(reverse("refugee:services"))
    return render(request, "refugee/transfer_reservation.html", {"form": form, "transfer": transfer})


@refugee_access()
def delete_transfer_service_reservation(request, refugee, reservation_id):
    TransferServiceReservation.objects.filter(id=reservation_id, refugee=refugee).delete()
    return redirect(reverse("refugee:services"))
