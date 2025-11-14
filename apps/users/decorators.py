from functools import wraps
from django.http import HttpResponse

def check_roles(*roles):
    def decorator(function):
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated and any(user.role == role for role in roles):
                return function(request, *args, **kwargs)
            else:
                return HttpResponse('Access denied', status=403)
        return wrapper
    return decorator
