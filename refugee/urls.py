from django.urls import path

from refugee.views import profile

app_name = "refugee"
urlpatterns = [
    path("profile", profile, name="profile"),
]
