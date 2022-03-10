from django.urls import path

from refugee.views import reserve_transfer_service, services

app_name = "refugee"
urlpatterns = [
    path("services", services, name="services"),
    path("reserve_transfer_service/<int:transfer_id>", reserve_transfer_service, name="reserve_transfer_service"),
]
