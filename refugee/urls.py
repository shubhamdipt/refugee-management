from django.urls import path

from refugee.views import (
    delete_transfer_service_reservation,
    reserve_transfer_service,
    services,
)

app_name = "refugee"
urlpatterns = [
    path("services", services, name="services"),
    path("reserve_transfer_service/<int:transfer_id>", reserve_transfer_service, name="reserve_transfer_service"),
    path(
        "delete_transfer_service_reservation/<int:reservation_id>",
        delete_transfer_service_reservation,
        name="delete_transfer_service_reservation",
    ),
]
