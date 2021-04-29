from . models import CoordinatorDetails
from . decorators import is_logged_in

def add_variable_to_context(request):
    if is_logged_in(request):
        coordinator_details = CoordinatorDetails.objects.get(username=request.session['is_coordinator'])
        return {
            'coordinator_details': coordinator_details
        }
    return {
        'hel':'he'
    }