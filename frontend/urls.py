from django.urls import path

from frontend.views import data_privacy, home, profile

app_name = "frontend"
urlpatterns = [
    path("", home, name="home"),
    path("profile", profile, name="profile"),
    path("data-privacy", data_privacy, name="data_privacy"),
]
