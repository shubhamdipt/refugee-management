from django.contrib import admin

from locations.models import City, Country, Route, RouteCities


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "country")


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("id", "cities_combination")


@admin.register(RouteCities)
class RouteCitiesAdmin(admin.ModelAdmin):
    list_display = ("id", "route", "city", "route_order")
