from django.shortcuts import redirect

def is_logged_in(request):
    return 'is_coordinator' in request.session