from django.urls import path

from frontend.views import data_privacy, home

app_name = "frontend"
urlpatterns = [
    path("", home, name="home"),
    path("data-privacy", data_privacy, name="data_privacy"),
]
