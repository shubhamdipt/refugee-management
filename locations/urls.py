from django.urls import path

from locations.views import api_cities

app_name = "locations"
urlpatterns = [
    path("cities", api_cities, name="api_cities"),
]
