from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from refugee.models import Refugee
from volunteer.models import Volunteer


def volunteer_access(view_func, redirect_url=None):
    @wraps(view_func)
    def view_wrapper(request, *args, **kwargs):
        user = Volunteer.objects.filter(account_user=request.user).first()
        if user:
            return view_func(request, user, *args, **kwargs)
        if redirect_url:
            return redirect(redirect_url)
        return HttpResponseForbidden("Not authorized. Contact Admin")

    return view_wrapper


def refugee_access(redirect_url=None):
    def access(view_func):
        @wraps(view_func)
        def view_wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if user := Refugee.objects.filter(account_user=request.user).first():
                    return view_func(request, user, *args, **kwargs)
            if redirect_url:
                return redirect(redirect_url)
            return HttpResponseForbidden("Not authorized. Contact Admin")

        return view_wrapper

    return access
