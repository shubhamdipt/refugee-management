from django.urls import path

from frontend.views import home

app_name = "frontend"
urlpatterns = [
    path("", home, name="home"),
]
