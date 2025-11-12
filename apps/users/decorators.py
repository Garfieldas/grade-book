from functools import wraps
from django.http import HttpResponseRedirect
from commons.models.roles import RoleChoices

def students_only(function):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if user.role == RoleChoices.STUDENT:
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return wrapper