from django.core.paginator import Paginator
from django.http import JsonResponse

from refugee.models import TransferReservation
from refugee_management.custom_access import refugee_access
from volunteer.models import TransferRouteDetails


@refugee_access()
def get_transfers(request, refugee):
    queryset = (
        TransferReservation.objects.filter(refugee=refugee)
        .select_related("transfer")
        .order_by("-transfer__start_time")
    )
    page = int(request.GET.get("page", 1))
    paginator = Paginator(queryset, 25)
    selected_results = paginator.get_page(page)
    paginator_to_dict = [i.as_dict() for i in selected_results]
    return JsonResponse({"results": paginator_to_dict})


@refugee_access()
def get_transfer_reservation_details(request, refugee, reservation_id):
    reservation = (
        TransferReservation.objects.filter(id=reservation_id, refugee=refugee)
        .select_related("from_city__city", "to_city__city")
        .first()
    )
    complete_transfer_details = list(
        TransferRouteDetails.objects.filter(transfer=reservation.transfer)
        .extra(select={"departure_date_string": "to_char(departure_time, 'DD/MM/YYY HH24:MI:SS')"})
        .values("id", "city__name", "city_id", "address", "departure_date_string")
        .order_by("departure_time")
    )
    details = []
    valid = False
    for i in complete_transfer_details:
        if i["city_id"] == reservation.from_city.city.id:
            valid = True
        if valid:
            details.append(i)
        if i["city_id"] == reservation.to_city.city.id:
            break
    return JsonResponse({"details": details})
