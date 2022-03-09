from django.urls import path

from refugee.views import services

app_name = "refugee"
urlpatterns = [
    path("services", services, name="services"),
]
