from django.urls import path
from django.utils.translation import gettext_lazy as _

from organization.forms import HelperForm, PickUpPointForm
from organization.models import Helper, OrganizationPickUpPoint
from organization.views import (
    EditView,
    add_transfer,
    delete_pick_up_point,
    delete_transfer,
    manage_helpers,
    manage_pick_up_points,
    services,
)
from organization.views_api import (
    add_pick_up_point,
    create_new_transfer,
    get_helpers,
    get_organization_transfer_details,
    get_pick_up_points,
    get_transfer_details,
    get_transfers,
)

app_name = "organization"
urlpatterns = [
    path("services", services, name="services"),
    path("delete-transfer/<int:transfer_id>", delete_transfer, name="delete_transfer"),
    path("delete-pick-up-point/<int:object_id>", delete_pick_up_point, name="delete_pick_up_point"),
    path("manage-pick-up-points", manage_pick_up_points, name="manage_pick_up_points"),
    path(
        "edit-pick-up-point/<int:object_id>",
        EditView.as_view(model=OrganizationPickUpPoint, form=PickUpPointForm, object_type=_("Pick up point")),
        name="edit_pick_up_point",
    ),
    path("manage-helpers", manage_helpers, name="manage_helpers"),
    path(
        "edit-helper/<int:object_id>",
        EditView.as_view(model=Helper, form=HelperForm, object_type=_("Helper")),
        name="edit_helper",
    ),
    path("add-transfer", add_transfer, name="add_transfer"),
    # APIs
    path("api/get-helpers", get_helpers, name="get_helpers"),
    path("api/get-pick-up-points", get_pick_up_points, name="get_pick_up_points"),
    path("api/add-pick-up-points", add_pick_up_point, name="add_pick_up_point"),
    path("api/create-new-transfer", create_new_transfer, name="create_new_transfer"),
    #
    path("api/get-transfers", get_transfers, name="get_transfers"),
    path("api/get-transfer-details/<int:transfer_id>", get_transfer_details, name="get_transfer_details"),
    path(
        "api/get-organization-transfer-details/<int:transfer_id>",
        get_organization_transfer_details,
        name="get_organization_transfer_details",
    ),
]
