from . models import Student
from django.shortcuts import redirect, render

def payment_required(view_func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if Student.objects.filter(payment=True, id=user.id).exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('student-payment')
    return wrap

def student_status(view_func):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_superuser == False:
            if user.admin_approval == 'approved':
                return view_func(request, *args, **kwargs)
            elif user.admin_approval == 'invalid':
                return redirect('edit-registration')
            else:
                return render(request, 'student/waiting-for-approval.html')
        else:
            return redirect('admin-login')
    return wrap