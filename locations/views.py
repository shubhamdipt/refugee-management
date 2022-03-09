from django.http import JsonResponse

from locations.models import City


def api_cities(request):
    cities = City.objects.order_by("name").select_related("country")
    ctx = {"results": [{"id": i.id, "text": f"{i.name}, {i.country.name}"} for i in cities]}
    return JsonResponse(ctx)
