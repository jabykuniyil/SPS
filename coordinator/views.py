from django.shortcuts import render, redirect
from . models import CoordinatorDetails, Batches
from student.models import Student
from django.contrib.auth.hashers import check_password
from django.core.files import File
from django.http import JsonResponse

# Create your views here.

def login(request):
    if request.session.has_key('is_coordinator'):
        return redirect(feed)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            coordinator_details = CoordinatorDetails.objects.filter(username=username).first()
            if coordinator_details is not None and check_password(password, coordinator_details.password):
                request.session['is_coordinator'] = True
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return render(request, 'coordinator/login.html')

def feed(request):
    if request.session.has_key('is_coordinator'):
        return render(request, 'coordinator/feed.html')
    else:
        return redirect(login)
    
def dashboard(request):
    if request.session.has_key('is_coordinator'):
        return render(request, 'coordinator/dashboard.html')
    else:
        return redirect(login)
def profile(request):
    if request.session.has_key('is_coordinator'):
        return render(request, 'coordinator/profile.html')
    else:
        return redirect(login)
    
def students(request):
    if request.session.has_key('is_coordinator'):
        students = Student.objects.filter(is_superuser=False)
        context = {'students' : students}
        return render(request, 'coordinator/students.html', context)
    else:
        return redirect(login)

def add_student(request):
    if request.session.has_key('is_coordinator'):
        if request.method == 'POST':
            fullname = request.POST['fullname']
            email = request.POST['email']
            phone = request.POST['phone']
            batch = request.POST['batch']
            age = request.POST['age']
            dob = request.POST['dob']
            gender = request.POST['gender']
            address = request.POST['address']
            father = request.POST['father']
            mother = request.POST['mother']
            domain = request.POST['domain']
            photo = request.FILES.get('photo')
            username = request.POST['username']
            password = request.POST['password']
            if Student.objects.filter(username=username).exists():
                return JsonResponse('username', safe=False)
            elif Student.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif Student.objects.filter(phone=phone).exists():
                return JsonResponse('phone', safe=False)
            else:
                Student.objects.create_user(fullname=fullname, email=email, phone=phone, batch=batch, age=age, dob=dob, gender=gender, address=address, father=father, mother=mother, domain=domain, photo=photo, username=username, password=password, payment=False, admin_approval='approved')
                return JsonResponse('true', safe=False)
        else:
            batches = Batches.objects.all()
            context = {'batches' : batches}
            return render(request, 'coordinator/add-student.html', context)
    else:
        return redirect(login)

def edit_student(request):
    if request.session.has_key('is_coordinator'):
        return render(request, 'coordinator/edit-student.html')
    else:
        return redirect(login)
    
def students_requests(request):
    if request.session.has_key('is_coordinator'):
        return render(request, 'coordinator/students-requests.html')
    else:
        return redirect(login)
    
def batches(request):
    if request.session.has_key('is_coordinator'):
        batches = Batches.objects.all()
        context = {'batches' : batches}
        return render(request, 'coordinator/batches.html', context)
    else:
        return redirect(login)
    
def batch_specific(request):
    if request.session.has_key('is_coordinator'):
        return render(request, 'coordinator/batch-specific.html')
    else:
        return redirect(login)
    
def add_batch(request):
    if request.session.has_key('is_coordinator'):
        if request.method == 'POST':
            name = request.POST['name']
            coordinator = request.POST['coordinator']
            capacity = request.POST['number']
            start_date = request.POST['startdate']
            Batches.objects.create(name=name, coordinator=coordinator, capacity=capacity, start_date=start_date)
            return JsonResponse('true', safe=False)
        else:
            coordinators = CoordinatorDetails.objects.all()
            context = {'coordinators' : coordinators}
            return render(request, 'coordinator/add-batch.html', context)
    else:
        return redirect(login)
    
def logout(request):
    if request.session.has_key('is_coordiantor'):
        return redirect(feed)
    else:
        request.session.flush()
        return redirect(login)