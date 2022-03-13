from django.urls import path

from volunteer.views import delete_transfer_service, services
from volunteer.views_api import (
    add_transfer_service,
    get_transfer_details,
    get_transfers,
)

app_name = "volunteer"
urlpatterns = [
    path("services", services, name="services"),
    path("add-transfer-service", add_transfer_service, name="add_transfer_service"),
    path("delete-transfer-service/<int:transfer_id>", delete_transfer_service, name="delete_transfer_service"),
    # APIs
    path("api/get-transfers", get_transfers, name="get_transfers"),
    path("api/get-transfer-details/<int:transfer_id>", get_transfer_details, name="get_transfer_details"),
]
