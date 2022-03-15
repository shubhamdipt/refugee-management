from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone

from locations.models import RouteCities
from organization.models import Transfer
from organization.seats_management import SeatsManagement
from refugee_management.custom_sql import get_custom_sql_results


def get_transfers(request):
    page = int(request.GET.get("page", 1))
    start_city = request.GET.get("start_city")
    end_city = request.GET.get("end_city")
    date_string = request.GET.get("date")
    seats = request.GET.get("seats")
    queryset = Transfer.objects.filter(active=True).order_by("start_time")
    if date_string:
        queryset = queryset.filter(start_time__date=datetime.strptime(date_string, "%d/%m/%Y").date())
    else:
        queryset = queryset.filter(start_time__gte=timezone.now())
    if start_city or end_city:
        if start_city and end_city:
            query = """
                SELECT a.route_id FROM locations_routecities a 
                INNER JOIN locations_routecities b ON a.route_id = b.route_id
                WHERE a.city_id = %s and b.city_id = %s and a.route_order < b.route_order;
            """
            results = get_custom_sql_results(query=query, params=(int(start_city), int(end_city)))
            route_ids = [i.route_id for i in results]
        else:
            valid_routes_query = RouteCities.objects.filter(city_id=int(start_city or end_city))
            route_ids = [i.route.id for i in valid_routes_query.distinct("route__id")]
        queryset = queryset.filter(organization_route__route__id__in=route_ids)

    if seats and start_city and end_city:
        seats = int(seats)
        valid_transfers = []
        for obj in queryset:
            seats_management = SeatsManagement(transfer=obj)
            if seats_management.determine_available_seats().get((int(start_city), int(end_city))) >= seats:
                valid_transfers.append(obj)
    else:
        valid_transfers = [i for i in queryset]

    paginator = Paginator(valid_transfers, 25)
    selected_results = paginator.get_page(page)
    paginator_to_dict = [i.as_dict() for i in selected_results]
    return JsonResponse({"results": paginator_to_dict})
