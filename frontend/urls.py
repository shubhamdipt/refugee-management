from django.urls import path

from frontend.views import data_privacy, home, services

app_name = "frontend"
urlpatterns = [
    path("", home, name="home"),
    path("services", services, name="services"),
    path("data-privacy", data_privacy, name="data_privacy"),
]
