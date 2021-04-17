from django.shortcuts import render, redirect
from . models import CoordinatorDetails, Batches, Week, Task, BatchSettings
from student.models import Student, Answer
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
    
def batch_specific(request, name):
    if request.session.has_key('is_coordinator'):
        students = Student.objects.filter(batch__name=name)
        weeks = BatchSettings.objects.filter(batch__name=name)
        all_weeks = Week.objects.all()
        batch = Batches.objects.get(name=name)
        context = {'students' : students, 'weeks' : weeks, 'batch' : batch, 'all_weeks' : all_weeks}
        return render(request, 'coordinator/batch-specific.html', context)
    else:
        return redirect(login)
    
def assign_week(request, id):
    if request.session.has_key('is_coordinator'):
        if request.method == 'POST':
            week_number = request.POST['week']
            week = Week.objects.get(week=week_number)
            batch = Batches.objects.get(id=id)
            week_no = int(week_number)
            last_week = BatchSettings.objects.filter(batch=batch).last()
            if BatchSettings.objects.filter(week=week, batch=batch).exists():
                return JsonResponse('exists', safe=False)
            elif BatchSettings.objects.filter(batch=batch).count() == 0:
                if week_no == 0:
                    BatchSettings.objects.create(week=week, batch=batch)
                    return JsonResponse('true', safe=False)
                else:
                    return JsonResponse('re-assign', safe=False)
            elif week_no-1 == last_week.week.week:
                BatchSettings.objects.create(week=week, batch=batch)
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return JsonResponse('true', safe=False)
    else:
        return redirect(login)
    
def add_batch(request):
    if request.session.has_key('is_coordinator'):
        if request.method == 'POST':
            name = request.POST['name']
            coordinator = request.POST['coordinator']
            capacity = request.POST['number']
            start_date = request.POST['startdate']
            Batches.objects.create(name=name, capacity=capacity, start_date=start_date)
            return JsonResponse('true', safe=False)
        else:
            coordinators = CoordinatorDetails.objects.all()
            context = {'coordinators' : coordinators}
            return render(request, 'coordinator/add-batch.html', context)
    else:
        return redirect(login)
    
def student_specific(request, id):
    if request.session.has_key('is_coordinator'):
        student = Student.objects.get(id=id)
        student_week = BatchSettings.objects.filter(batch=student.batch)
        weeks = []
        for x in student_week:
            weeks.append(x.week)
        context = {'student' : student, 'weeks' : weeks}
        return render(request, 'coordinator/student-specific.html', context)
    else:
        return redirect(login)

def student_task(request, studentid, weekid):
    if request.session.has_key('is_coordinator'):
        week = Week.objects.get(id=weekid)
        miscelleneous_task = Task.objects.filter(week=week, type_of_task='Miscelleneuos Task')
        personal_development = Task.objects.filter(week=week, type_of_task='Personal Development')
        technical_task = Task.objects.filter(week=week, type_of_task='Technical Task')
        miscelleneous_task_dict = {}
        personal_development_dict = {}
        technical_task_dict = {}
        student_answers = Answer.objects.filter(student_id=studentid, task__week=week)
        student = Student.objects.get(id=studentid)
        personal_answers = {}
        technical_answers = {}
        miscelleneous_answers = {}
        for x in student_answers:
            if x.task.type_of_task == 'Miscelleneuos Task':
                miscelleneous_answers[x.task.id] = x.answer
            if x.task.type_of_task == 'Personal Development':
                personal_answers[x.task.id] = x.answer
            if x.task.type_of_task == 'Technical Task':
                technical_answers[x.task.id] = x.answer
        for x in technical_task:
            technical_task_dict[x.id] = x.question
        for x in miscelleneous_task:
            miscelleneous_task_dict[x.id] = x.question
        for x in personal_development:
            personal_development_dict[x.id] = x.question
        context = {
            'personal_tasks' : personal_development_dict,
            'technical_tasks' : technical_task_dict,
            'miscelleneous_tasks' : miscelleneous_task_dict,
            'personal_answers' : personal_answers,
            'technical_answers' : technical_answers,
            'miscelleneous_answers' : miscelleneous_answers,
            'student' : student,
            'week' : week
            }
        return render(request, 'coordinator/student-task.html', context)
    else:
        return redirect(login)

def choose_week(request):
    if request.session.has_key('is_coordinator'):
        weeks = Week.objects.all()
        context = { 'weeks' : weeks}
        return render(request, 'coordinator/choose-week.html', context)
    else:
        return redirect(login)
    
def add_week(request):
    if request.session.has_key('is_coordinator'):
        if request.method == 'POST':
            week = request.POST['week']
            if Week.objects.filter(week=week).exists():
                return JsonResponse('week', safe=False)
            else:
                Week.objects.create(week=week)
                return JsonResponse('true', safe=False)
    else:
        return redirect(login)
    
def task_specific(request, weekid):
    if request.session.has_key('is_coordinator'):
        if request.method == 'POST':
            qeustion = request.POST['textareaValue']
            type_of_task = request.POST['typeOfTask']
            Task.objects.create(question=qeustion, week_id=weekid, type_of_task=type_of_task)
            return JsonResponse('true', safe=False)
        else:
            week_id = Week.objects.get(id=weekid)
            miscelleneous_task = Task.objects.filter(week=week_id, type_of_task='Miscelleneuos Task')
            personal_development = Task.objects.filter(week=week_id, type_of_task='Personal Development')
            technical_task = Task.objects.filter(week=week_id, type_of_task='Technical Task')
            miscelleneous_task_dict = {}
            personal_development_dict = {}
            technical_task_dict = {}
            for x in technical_task:
                technical_task_dict[x.id] = x.question
            for x in miscelleneous_task:
                miscelleneous_task_dict[x.id] = x.question
            for x in personal_development:
                personal_development_dict[x.id] = x.question
            context = {'weekid' : week_id.id, 'miscelleneousTask' : miscelleneous_task_dict, 'personalDevelopment' : personal_development_dict, 'technicalTask' : technical_task_dict}
            return render(request, 'coordinator/task-specific.html', context)
    else:
        return redirect(login)

def edit_task(request, weekid, taskid):
    if request.session.has_key('is_coordinator'):
        if request.method == 'POST':
            question = request.POST['editareaValue']
            Task.objects.filter(week_id=weekid, id=taskid).update(question=question)
            return JsonResponse('true', safe=False)
        else:
            return JsonResponse('true', safe=False)
    else:   
        return redirect(login)
    
def delete_task(request, weekid, taskid):
    if request.session.has_key('is_coordinator'):
        task = Task.objects.filter(week_id=weekid, id=taskid)
        task.delete()
        return redirect(task_specific, weekid=weekid)
    else:
        return redirect(login)
    
def logout(request):
    if request.session.has_key('is_coordiantor'):
        return redirect(feed)
    else:
        request.session.flush()
        return redirect(login)