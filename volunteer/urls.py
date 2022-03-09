from django.urls import path

from volunteer.views import profile

app_name = "volunteer"
urlpatterns = [
    path("profile", profile, name="profile"),
]
