from django.urls import path

from volunteer.views import add_transfer_service, delete_transfer_service, services

app_name = "volunteer"
urlpatterns = [
    path("services", services, name="services"),
    path("add_transfer_service", add_transfer_service, name="add_transfer_service"),
    path("delete_transfer_service/<int:transfer_id>", delete_transfer_service, name="delete_transfer_service"),
]
