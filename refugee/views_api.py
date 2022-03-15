from django.http import JsonResponse

from organization.models import TransferRouteDetails
from refugee.models import TransferReservation
from refugee_management.custom_access import refugee_access


@refugee_access()
def get_transfers(request, refugee):
    queryset = (
        TransferReservation.objects.filter(refugee=refugee)
        .select_related("transfer")
        .order_by("-transfer__start_time")
    )
    results = [i.as_dict() for i in queryset]
    return JsonResponse({"results": results})


@refugee_access()
def get_transfer_reservation_details(request, refugee, reservation_id):
    reservation = (
        TransferReservation.objects.filter(id=reservation_id, refugee=refugee)
        .select_related("from_city__city", "to_city__city")
        .first()
    )
    details = []
    valid = False
    for location in TransferRouteDetails.objects.filter(transfer=reservation.transfer).order_by("departure_time"):
        if location.city.id == reservation.from_city.city.id:
            valid = True
        if valid:
            details.append(location.as_dict())
        if location.city.id == reservation.to_city.city.id:
            break
    return JsonResponse(
        {
            "details": details,
            "transfer": reservation.transfer.as_dict(helper_view=True, refugee_view=True),
            "reservation_id": reservation.id,
            "seats": reservation.seats,
        }
    )
