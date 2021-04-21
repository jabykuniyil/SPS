from . utils import is_logged_in
from django.shortcuts import redirect

def login_required(func):
    def wrapped_func(request, *args, **kwargs):
        if is_logged_in(request):
            return func(request, *args, **kwargs)
        else:
            return redirect('coordinator-login')
    return wrapped_func
    