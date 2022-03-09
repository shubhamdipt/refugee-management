from functools import wraps

from django.http import HttpResponseForbidden

from refugee.models import Refugee
from volunteer.models import Volunteer


def volunteer_access(view_func):
    @wraps(view_func)
    def view_wrapper(request, *args, **kwargs):
        user = Volunteer.objects.filter(account_user=request.user).first()
        if user:
            return view_func(request, user, *args, **kwargs)
        return HttpResponseForbidden("Not authorized. Contact Admin")

    return view_wrapper


def refugee_access(view_func):
    @wraps(view_func)
    def view_wrapper(request, *args, **kwargs):
        user = Refugee.objects.filter(account_user=request.user).first()
        if user:
            return view_func(request, user, *args, **kwargs)
        return HttpResponseForbidden("Not authorized. Contact Admin")

    return view_wrapper
