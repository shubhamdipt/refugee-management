from django.http import JsonResponse

from locations.models import City


def api_cities(request):
    cities = City.objects.order_by("name").select_related("country")
    ctx = {"results": [{"id": i.id, "text": i.name} for i in cities]}
    return JsonResponse(ctx)
