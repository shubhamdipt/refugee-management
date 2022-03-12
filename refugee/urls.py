from django.urls import path

from refugee.views import delete_transfer_reservation, reserve_transfer, services
from refugee.views_api import get_transfer_reservation_details, get_transfers

app_name = "refugee"
urlpatterns = [
    path("services", services, name="services"),
    path("reserve-transfer/<int:transfer_id>", reserve_transfer, name="reserve_transfer"),
    path(
        "delete-transfer-reservation/<int:reservation_id>",
        delete_transfer_reservation,
        name="delete_transfer_reservation",
    ),
    # APIs
    path("api/get-transfers", get_transfers, name="get_transfers"),
    path(
        "api/get-transfer-reservation-details/<int:reservation_id>",
        get_transfer_reservation_details,
        name="get_transfer_reservation_details",
    ),
]
