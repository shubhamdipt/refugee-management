from django.shortcuts import redirect, render, reverse

from organization.forms import PickUpPointForm
from organization.models import Helper, OrganizationPickUpPoint, Transfer
from refugee_management.custom_access import (
    organization_helper_access,
    organization_helper_admin_access,
)


@organization_helper_access()
def services(request, helper):
    return render(
        request,
        "organization/services.html",
        {"vehicle_types": Transfer.VEHICLE_CHOICES, "admin": helper.account_type == Helper.ADMIN},
    )


@organization_helper_access()
def delete_transfer_service(request, helper, transfer_id):
    Transfer.objects.filter(id=transfer_id, helper=helper).delete()
    return redirect(reverse("organization:services"))


@organization_helper_admin_access()
def manage_pick_up_points(request, helper):
    return render(
        request,
        "organization/pick_up_points.html",
        {"helper": helper, "form": PickUpPointForm()},
    )


@organization_helper_admin_access()
def delete_pick_up_point(request, helper, object_id):
    OrganizationPickUpPoint.objects.filter(id=object_id, organization=helper.organization).delete()
    return redirect(reverse("organization:manage_pick_up_points"))
