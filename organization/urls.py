from django.urls import path

from organization.views import (
    delete_pick_up_point,
    delete_transfer_service,
    manage_pick_up_points,
    services,
)
from organization.views_api import (
    add_pick_up_point,
    add_transfer_service,
    get_pick_up_points,
    get_transfer_details,
    get_transfers,
)

app_name = "organization"
urlpatterns = [
    path("services", services, name="services"),
    path("add-transfer-service", add_transfer_service, name="add_transfer_service"),
    path("delete-transfer-service/<int:transfer_id>", delete_transfer_service, name="delete_transfer_service"),
    path("delete-pick-up-point/<int:object_id>", delete_pick_up_point, name="delete_pick_up_point"),
    path("manage-pick-up-points", manage_pick_up_points, name="manage_pick_up_points"),
    # APIs
    path("api/get-pick-up-points", get_pick_up_points, name="get_pick_up_points"),
    path("api/add-pick-up-points", add_pick_up_point, name="add_pick_up_point"),
    path("api/get-transfers", get_transfers, name="get_transfers"),
    path("api/get-transfer-details/<int:transfer_id>", get_transfer_details, name="get_transfer_details"),
]
