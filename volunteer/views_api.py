from datetime import datetime

from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST

from locations.models import Route
from refugee_management.custom_access import volunteer_access
from volunteer.models import Transfer, TransferRouteDetails, VolunteerRoute


@volunteer_access()
def get_transfers(request, volunteer):
    page = int(request.GET.get("page", 1))
    queryset = Transfer.objects.filter(volunteer_route__volunteer=volunteer).order_by("-start_time")
    paginator = Paginator(queryset, 25)
    selected_results = paginator.get_page(page)
    paginator_to_dict = [i.as_dict(show_details=True) for i in selected_results]
    return JsonResponse({"results": paginator_to_dict})


@volunteer_access()
def get_transfer_details(request, volunteer, transfer_id):
    transfer = Transfer.objects.get(id=transfer_id, volunteer_route__volunteer=volunteer)
    ctx = {
        "details": list(
            TransferRouteDetails.objects.filter(transfer=transfer)
            .extra(select={"departure_date_string": "to_char(departure_time, 'DD/MM/YYY HH24:MI:SS')"})
            .values("id", "city__name", "address", "departure_date_string")
            .order_by("departure_time")
        ),
    }
    return JsonResponse(ctx)


@transaction.atomic
@volunteer_access()
@require_POST
def add_transfer_service(request, volunteer):
    current_tz = timezone.get_current_timezone()
    try:
        transfer_refugees = request.POST.get("transfer-refugees")
        vehicle_type = request.POST.get("vehicle_type")
        vehicle_registration_number = request.POST.get("vehicle_registration_number")
        stopovers = []
        count = 1
        while True:
            city_key = f"city-{count}"
            datetime_key = f"datetime-{count}"
            address_key = f"address-{count}"
            city_id = request.POST.get(city_key)
            datetime_string = request.POST.get(datetime_key)
            address = request.POST.get(address_key)
            if city_id and datetime_string and address:
                stopovers.append(
                    (
                        city_id,
                        datetime.strptime(datetime_string, "%d/%m/%Y %H:%M").replace(tzinfo=current_tz),
                        address,
                    )
                )
                count += 1
            elif all(v is None for v in [city_id, datetime_string, address]):
                break
            else:
                raise ValueError("Incomplete form filled. Please check the form again.")

        datetime_strings = [i[1] for i in stopovers]
        if len(stopovers) < 2:
            raise ValueError("Minimum two stopovers are required.")
        if sorted(datetime_strings) != datetime_strings or len(datetime_strings) != len(set(datetime_strings)):
            raise ValueError("Invalid time found. Please check the order of the time entered for each stopover.")
        if not transfer_refugees:
            raise ValueError("Missing number of passengers.")
        if not vehicle_type:
            raise ValueError("Missing vehicle type.")
        route, _ = Route.objects.get_or_create_with_cities_ids(cities_ids=[i[0] for i in stopovers])
        volunteer_route, _ = VolunteerRoute.objects.get_or_create(route=route, volunteer=volunteer)
        obj = Transfer.objects.create(
            volunteer_route=volunteer_route,
            total_seats=int(transfer_refugees),
            start_time=datetime_strings[0],
            vehicle=int(vehicle_type) if vehicle_type else None,
            vehicle_registration_number=vehicle_registration_number,
        )
        transfer_route_objects = []
        for stopover in stopovers:
            transfer_route_objects.append(
                TransferRouteDetails(
                    transfer=obj, city_id=stopover[0], departure_time=stopover[1], address=stopover[2]
                )
            )
        TransferRouteDetails.objects.bulk_create(transfer_route_objects)
    except IntegrityError:
        error = "Invalid form submitted. Same cities have been entered more than once as stopovers."
        return JsonResponse({"error": error})
    except ValueError as e:
        error = str(e)
        return JsonResponse({"error": error})
    return JsonResponse({"success": "Form has been successfully submitted.", "instance": obj.as_dict()})
