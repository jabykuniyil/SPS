from django.shortcuts import render, redirect
from . models import CoordinatorDetails, Batches, Week, Task
from student.models import Student
from django.contrib.auth.hashers import check_password
from django.core.files import File
from django.http import JsonResponse
import json

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
        students = Student.objects.filter(admin_approval='pending', is_superuser=False)
        context = {'students' : students}
        return render(request, 'coordinator/students-requests.html', context)
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
    
def batch_tasks(request):
    if request.session.has_key('is_coordinator'):
        batches = Batches.objects.all()
        context = {'batches' : batches}
        return render(request, 'coordinator/batch-tasks.html', context)
    else:
        return redirect(login)
    
def choose_week(request, id):
    if request.session.has_key('is_coordinator'):
        batch = Batches.objects.get(id=id)
        weeks = Week.objects.filter(batch=batch)
        context = {'id' : batch.id, 'weeks' : weeks}
        return render(request, 'coordinator/choose-week.html', context)
    else:
        return redirect(login)
    
def add_week(request, id):
    if request.session.has_key('is_coordinator'):
        if request.method == 'POST':
            week = request.POST['week']
            batch = Batches.objects.get(id=id)
            Week.objects.create(batch=batch, week=week)
            return JsonResponse('true', safe=False)
    else:
        return redirect(login)
    
def task_specific(request, batchid, weekid):
    if request.session.has_key('is_coordinator'):
        if request.method == 'POST':
            qeustion = request.POST['textareaValue']
            type_of_task = request.POST['typeOfTask']
            Task.objects.create(question=qeustion, week_id=weekid, batch_id=batchid, type_of_task=type_of_task)
            return JsonResponse('true', safe=False)
        else:
            week_id = Week.objects.get(id=weekid)
            batch_id = Batches.objects.get(id=batchid)
            miscelleneous_task = Task.objects.filter(batch=batch_id, week=week_id, type_of_task='Miscelleneuos Task')
            personal_development = Task.objects.filter(batch=batch_id, week=week_id, type_of_task='Personal Development')
            technical_task = Task.objects.filter(batch=batch_id, week=week_id, type_of_task='Technical Task')
            miscelleneous_task_dict = {}
            personal_development_dict = {}
            technical_task_dict = {}
            for x in technical_task:
                technical_task_dict[x.id] = x.question
            for x in miscelleneous_task:
                miscelleneous_task_dict[x.id] = x.question
            for x in personal_development:
                personal_development_dict[x.id] = x.question
            context = {'weekid' : week_id.id, 'batchid' : batch_id.id, 'miscelleneousTask' : miscelleneous_task_dict, 'personalDevelopment' : personal_development_dict, 'technicalTask' : technical_task_dict}
            return render(request, 'coordinator/task-specific.html', context)
    else:
        return redirect(login)

def edit_task(request, weekid, batchid, taskid):
    if request.session.has_key('is_coordinator'):
        if request.method == 'POST':
            question = request.POST['editareaValue']
            Task.objects.filter(week_id=weekid, batch_id=batchid, id=taskid).update(question=question)
            return JsonResponse('true', safe=False)
        else:
            return JsonResponse('true', safe=False)
    else:   
        return redirect(login)
    
def delete_task(request, batchid, weekid, taskid):
    if request.session.has_key('is_coordinator'):
        task = Task.objects.filter(batch_id=batchid, week_id=weekid, id=taskid)
        task.delete()
        return redirect(task_specific, batchid=batchid, weekid=weekid)
    else:
        return redirect(login)
    
def logout(request):
    if request.session.has_key('is_coordiantor'):
        return redirect(feed)
    else:
        request.session.flush()
        return redirect(login)