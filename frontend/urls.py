from django.urls import path

from frontend.views import data_privacy, home, services
from frontend.views_api import get_transfers

app_name = "frontend"
urlpatterns = [
    path("", home, name="home"),
    path("services", services, name="services"),
    path("data-privacy", data_privacy, name="data_privacy"),
    # APIs
    path("api/get-transfers", get_transfers, name="get_transfers"),
]
