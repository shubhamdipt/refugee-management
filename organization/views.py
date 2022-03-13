from django.shortcuts import redirect, render, reverse

from refugee_management.custom_access import volunteer_access
from volunteer.models import Transfer


@volunteer_access()
def services(request, volunteer):
    return render(request, "volunteer/services.html", {"vehicle_types": Transfer.VEHICLE_CHOICES})


@volunteer_access()
def delete_transfer_service(request, volunteer, transfer_id):
    Transfer.objects.filter(id=transfer_id, volunteer_route__volunteer=volunteer).delete()
    return redirect(reverse("volunteer:services"))
