from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group, User

def unauthenticated_user(view_func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized!")

        return wrapper

    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        print(request.user.groups.exists())
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'staff':
            return redirect('user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function
