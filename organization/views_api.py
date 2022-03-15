from datetime import datetime

from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import make_aware
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from locations.models import Route
from organization.forms import PickUpPointForm, TransferForm
from organization.models import (
    Helper,
    OrganizationPickUpPoint,
    OrganizationRoute,
    Transfer,
    TransferRouteDetails,
)
from refugee_management.custom_access import (
    organization_helper_access,
    organization_helper_admin_access,
)


@organization_helper_admin_access()
def get_pick_up_points(request, helper):
    queryset = OrganizationPickUpPoint.objects.filter(organization=helper.organization).order_by(
        "city__country__name", "city__name"
    )
    results = [
        {"country": i.city.country.name, "city": i.city.name, "address": i.address, "id": i.id} for i in queryset
    ]
    return JsonResponse({"results": results})


@organization_helper_admin_access()
def get_helpers(request, helper):
    queryset = Helper.objects.filter(organization=helper.organization).order_by("account_user__email")
    results = [i.as_dict() for i in queryset]
    return JsonResponse({"results": results})


@organization_helper_admin_access()
@require_POST
def add_pick_up_point(request, helper):
    ctx = {}
    form = PickUpPointForm(request.POST)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.organization = helper.organization
        obj.save()
        ctx["success"] = "Pick up point has been successfully added."
    return JsonResponse(ctx)


@organization_helper_access()
def get_transfers(request, helper):
    queryset = Transfer.objects.filter(helper=helper).order_by("-start_time")
    results = [i.as_dict(show_details=True) for i in queryset]
    return JsonResponse({"results": results})


@organization_helper_access()
def get_transfer_details(request, helper, transfer_id):
    transfer = Transfer.objects.get(id=transfer_id, helper=helper)
    ctx = {
        "object": transfer.as_dict(show_details=True),
        "details": [
            i.as_dict() for i in TransferRouteDetails.objects.filter(transfer=transfer).order_by("departure_time")
        ],
    }
    return JsonResponse(ctx)


@organization_helper_admin_access()
def get_organization_transfer_details(request, helper, transfer_id):
    transfer = Transfer.objects.get(id=transfer_id, organization_route__organization=helper.organization)
    ctx = {
        "object": transfer.as_dict(show_details=True),
        "details": [
            i.as_dict() for i in TransferRouteDetails.objects.filter(transfer=transfer).order_by("departure_time")
        ],
    }
    return JsonResponse(ctx)


@transaction.atomic
@organization_helper_admin_access()
@require_POST
def create_new_transfer(request, helper):
    current_tz = timezone.get_current_timezone()
    try:
        stopovers_details = []
        count = 1
        while True:
            stopover_key = f"stopover-{count}"
            date_key = f"date-{count}"
            time_key = f"time-{count}"
            stopover_id = request.POST.get(stopover_key)
            date_string = request.POST.get(date_key)
            time_string = request.POST.get(time_key)
            if stopover_id and date_string and time_string:
                stopovers_details.append(
                    (
                        OrganizationPickUpPoint.objects.get(id=stopover_id, organization=helper.organization),
                        make_aware(datetime.strptime(f"{date_string} {time_string}", "%d/%m/%Y %H:%M")),
                    )
                )
                count += 1
            # Stop when all fields are found empty
            elif all(v is None for v in [stopover_id, date_string, time_string]):
                break
            # Raise when any field is found empty
            else:
                raise ValueError(_("Incomplete form filled. Please check the form again."))

        datetime_strings = [i[1] for i in stopovers_details]
        if len(stopovers_details) < 2:
            raise ValueError(_("Minimum two stopovers are required."))
        if sorted(datetime_strings) != datetime_strings or len(datetime_strings) != len(set(datetime_strings)):
            raise ValueError(_("Invalid time found. Please check the order of the time entered for each stopover."))

        # Create transfer
        transfer_form = TransferForm(helper=helper, data=request.POST)
        if transfer_form.is_valid():
            # Create route
            route, route_created = Route.objects.get_or_create_with_cities_ids(
                cities_ids=[i[0].city.id for i in stopovers_details]
            )
            organization_route, org_route_created = OrganizationRoute.objects.get_or_create(
                route=route, organization=helper.organization
            )

            obj = transfer_form.save(commit=False)
            obj.organization_route = organization_route
            obj.start_time = datetime_strings[0]
            obj.save()
            transfer_route_objects = []
            for stopover in stopovers_details:
                transfer_route_objects.append(
                    TransferRouteDetails(
                        transfer=obj, city=stopover[0].city, departure_time=stopover[1], address=stopover[0].address
                    )
                )
            TransferRouteDetails.objects.bulk_create(transfer_route_objects)
        else:
            return JsonResponse(
                {
                    "error": transfer_form.errors.get("__all__")[0]
                    if transfer_form.errors.get("__all__")
                    else _("Invalid form submitted.")
                }
            )
    except IntegrityError:
        error = _("Invalid form submitted. Same cities have been entered more than once as stopovers.")
        return JsonResponse({"error": error})
    except ValueError as e:
        error = str(e)
        return JsonResponse({"error": error})
    except OrganizationPickUpPoint.DoesNotExist:
        return JsonResponse({"error": _("Pick up point does not exist for this organization.")})
    return JsonResponse({"success": _("Transfer has been successfully submitted.")})
