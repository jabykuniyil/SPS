from django.shortcuts import render, redirect
from . models import CoordinatorDetails, Batches, Week, Task, BatchSettings, ReviewColors
from student.models import Student, Answer, Review, CommentAnswer
from django.contrib.auth.hashers import check_password
from django.core.files import File
from django.http import JsonResponse
from . decorators import login_required
from . utils import is_logged_in
from django.db.models import Q
from django.core import serializers
from . forms import CommentForm
from django.http import HttpResponse
import json, datetime

# Create your views here.

def coordinator(request):
    if is_logged_in(request):
        return redirect(dashboard)
    return redirect(login)

def login(request):
    if is_logged_in(request):
        return redirect(profile)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        coordinator_details = CoordinatorDetails.objects.filter(username=username).first()
        if coordinator_details is not None and check_password(password, coordinator_details.password):
            request.session['is_coordinator'] = username
            return JsonResponse('true', safe=False)
        return JsonResponse('false', safe=False)
    return render(request, 'coordinator/login.html')

@login_required
def search(request):
    if request.method == 'GET':
        letter = request.GET['letter']
        student_dict = {}
        student = Student.objects.filter(fullname__icontains=letter)
        for x in student:
            student_dict[x.batch.id] = x.batch.name
        students = serializers.serialize("json", student)
        serialized_student = json.loads(students)
        for x in serialized_student:
            x['fields']['batch_name'] = student_dict[x['fields']['batch']]
        context = {'students' : json.dumps(serialized_student), 'status' : 'true'}
        return JsonResponse(context)
    
@login_required
def dashboard(request):
    students = Student.objects.filter(is_superuser=False)
    colors = ReviewColors.objects.all()
    batches = Batches.objects.all()
    context = {'colors' : colors, 'students' : students, 'batches' : batches}
    return render(request, 'coordinator/dashboard.html', context)
    
@login_required
def students(request):
    students = Student.objects.filter(is_superuser=False)
    context = {'students' : students}
    return render(request, 'coordinator/students.html', context)

@login_required
def add_student(request):
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
        Student.objects.create_user(fullname=fullname, email=email, phone=phone, batch=batch, age=age, dob=dob, gender=gender, address=address, father=father, mother=mother, domain=domain, photo=photo, username=username, password=password, payment=False, admin_approval='approved')
        return JsonResponse('true', safe=False)
    batches = Batches.objects.all()
    context = {'batches' : batches}
    return render(request, 'coordinator/add-student.html', context)

@login_required
def edit_student(request):
    return render(request, 'coordinator/edit-student.html')
    
@login_required
def students_requests(request):
    students = Student.objects.filter(admin_approval='pending', is_superuser=False)
    context = {'students' : students}
    return render(request, 'coordinator/students-requests.html', context)
    
@login_required    
def batches(request):
    batches = Batches.objects.all()
    context = {'batches' : batches}
    return render(request, 'coordinator/batches.html', context)

@login_required    
def batch_specific(request, name):
    students = Student.objects.filter(batch__name=name)
    weeks = BatchSettings.objects.filter(batch__name=name)
    all_weeks = Week.objects.all()
    batch = Batches.objects.get(name=name)
    context = {'students' : students, 'weeks' : weeks, 'batch' : batch, 'all_weeks' : all_weeks}
    return render(request, 'coordinator/batch-specific.html', context)

@login_required    
def assign_week(request, id):
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
            return JsonResponse('re-assign', safe=False)
        elif week_no-1 == last_week.week.week:
            BatchSettings.objects.create(week=week, batch=batch)
            return JsonResponse('true', safe=False)
        return JsonResponse('false', safe=False)
    return JsonResponse('true', safe=False)

@login_required
def edit_week_assign(request, weekid, batchid):
    BatchSettings.objects.filter(week_id=weekid, batch_id=batchid).delete()
    batch = Batches.objects.get(id=batchid)
    return redirect(batch_specific, batch.name)
        
@login_required  
def add_batch(request):
    if request.method == 'POST':
        name = request.POST['name']
        coordinator = request.POST['coordinator']
        capacity = request.POST['number']
        start_date = request.POST['startdate']
        Batches.objects.create(name=name, capacity=capacity, start_date=start_date)
        return JsonResponse('true', safe=False)
    coordinators = CoordinatorDetails.objects.all()
    context = {'coordinators' : coordinators}
    return render(request, 'coordinator/add-batch.html', context)

@login_required   
def student_specific(request, id):
    if request.method == 'POST':
        days = request.POST['days']
        Student.objects.filter(id=id).update(admin_approval='suspended')
        return redirect(student_specific, id)
    student = Student.objects.get(id=id)
    student_week = BatchSettings.objects.filter(batch=student.batch)
    student_review = Review.objects.filter(student_id=id)
    review = []
    for x in student_review:
        review.append(x)
    weeks = []
    for x in student_week:
        weeks.append(x.week)
        for y in student_review:
            if y.week.week == x.week.week:
                x.week.is_review = True
                break
    batches = Batches.objects.all()
    batches_list = []
    for x in batches:
        if x.name == student.batch.name:
            batches_list.append(x)
            batches_list.remove(student.batch)
        else:
            batches_list.append(x)
    context = {'student' : student, 'weeks' : weeks, 'review' : review, 'batches' : batches_list}
    return render(request, 'coordinator/student-specific.html', context)

@login_required
def remove_suspension(request, id):
    Student.objects.filter(id=id, admin_approval='suspended').update(admin_approval='approved')
    return redirect(student_specific, id)

@login_required
def terminate_student(request, id):
    Student.objects.filter(id=id).update(admin_approval='terminated')
    return redirect(student_specific, id)

@login_required
def remove_termination(request, id):
    Student.objects.filter(id=id).update(admin_approval='approved')
    return redirect(student_specific, id)

@login_required
def student_placed(request, id):
    if request.method == 'POST':
        Student.objects.filter(id=id).update(admin_approval='placed')
        return redirect(student_specific, id)

@login_required
def task_id(request, id):
    task_id = request.GET['task_id']
    student = Student.objects.get(id=id)
    student.task_id = task_id
    request.session['task_id'] = student.task_id
    return JsonResponse('true', safe=False)

@login_required
def student_task(request, studentid, weekid):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            CommentAnswer.objects.create(comment=request.POST['comment'], student_id=studentid, task_id=request.session['comment_task_id'], coordinator=request.session['is_coordinator'])
            return redirect(student_task, studentid=studentid, weekid=weekid)
    form = CommentForm()
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
    student_answer = Answer.objects.filter(student_id=studentid)
    time = datetime.datetime.now()
    edit_dict = {}
    for x in student_answer:
        answer_time = datetime.datetime.strptime(x.time, '%Y-%m-%d %H:%M:%S')
        edit_dict[answer_time] = x
    date_time_keys = edit_dict.keys()
    key_editor = Answer.objects.filter(time__in=date_time_keys).order_by('-time')
    editor_date_time = {}
    for x in key_editor:
        x_time = datetime.datetime.strptime(x.time, '%Y-%m-%d %H:%M:%S')
        time_dif = time - x_time
        x.day = time_dif.days
        x.hour = time_dif.seconds//3600
        x.minute = (time_dif.seconds//60)%60
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
        'week' : week,
        'edit' : key_editor,
        'form' : form
        }
    return render(request, 'coordinator/student-task.html', context)

@login_required    
def student_review(request, studentid, weekid):
    if request.method == 'POST':
        coordinator_review = request.POST['coordinator_review']
        score = request.POST['score']
        int_score = int(score)
        review_color = ReviewColors.objects.filter(score_from__lte=int_score, score_to__gte=int_score).first()
        Review.objects.create(coordinator_review=coordinator_review, coordinator=request.session['is_coordinator'], score=int_score, student_id=studentid, week_id=weekid, color_id=review_color.id)
        color = {'status' : 'review', 'color' : review_color.color, 'description' : review_color.description}
        return JsonResponse(color)
    
@login_required
def edit_review(request, studentId, week):
    if request.method == 'POST':
        coordinator_review = request.POST['coordinator_review']
        score = request.POST['score']
        int_score = int(score)
        date = datetime.date.today()
        review_color = ReviewColors.objects.filter(score_from__lte=int_score, score_to__gte=int_score).first()
        Review.objects.filter(student_id=studentId, week__week=week).update(coordinator_review=coordinator_review, score=score, color=review_color, coordinator_date=date)
        return JsonResponse('true', safe=False)
    return JsonResponse('true', safe=False)

@login_required
def shift_batch(request, id):
    if request.method == 'POST':
        batch = request.POST['batch']
        student = Student.objects.filter(id=id).update(batch_id=batch)
        return JsonResponse('true', safe=False)
            
@login_required
def choose_week(request):
    weeks = Week.objects.all()
    context = { 'weeks' : weeks}
    return render(request, 'coordinator/choose-week.html', context)

@login_required    
def add_week(request):
    if request.method == 'POST':
        week = request.POST['week']
        if Week.objects.filter(week=week).exists():
            return JsonResponse('week', safe=False)
        Week.objects.create(week=week)
        return JsonResponse('true', safe=False)

@login_required   
def task_specific(request, weekid):
    if request.method == 'POST':
        qeustion = request.POST['textareaValue']
        type_of_task = request.POST['typeOfTask']
        Task.objects.create(question=qeustion, week_id=weekid, type_of_task=type_of_task)
        return JsonResponse('true', safe=False)
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
    context = {
        'weekid' : week_id.id,
        'miscelleneousTask' : miscelleneous_task_dict,
        'personalDevelopment' : personal_development_dict,
        'technicalTask' : technical_task_dict
        }
    return render(request, 'coordinator/task-specific.html', context)

@login_required
def edit_task(request, weekid, taskid):
    if request.method == 'POST':
        question = request.POST['editareaValue']
        Task.objects.filter(week_id=weekid, id=taskid).update(question=question)
        return JsonResponse('true', safe=False)
    return JsonResponse('true', safe=False)

@login_required   
def delete_task(request, weekid, taskid):
    task = Task.objects.filter(week_id=weekid, id=taskid)
    task.delete()
    return redirect(task_specific, weekid=weekid)

@login_required   
def edit_answer(request, taskid, studentid):
    if request.method == 'POST':
        task = Task.objects.get(id=taskid)
        answer = request.POST['answer']
        student = Student.objects.get(id=studentid)
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Answer.objects.filter(task=task, student=student).update(answer=answer, student=student, time=time, editor=request.session['is_coordinator'])
        return JsonResponse('true', safe=False)

@login_required    
def add_color(request):
    if request.method == 'POST':
        color = request.POST['color']
        description = request.POST['description']
        post_score_from = request.POST['score_from']
        post_score_to = request.POST['score_to']
        review = ReviewColors.objects.all()
        if post_score_from == '' and post_score_to == '':
            ReviewColors.objects.create(color=color, description=description)
            modal = ReviewColors.objects.filter(color=color).last()
            modal_context = {'status' : 'modal', 'color' : modal.color}
            return JsonResponse(modal_context)
        score_from = int(post_score_from)
        score_to = int(post_score_to)
        if score_from > score_to:
            return JsonResponse('not_comparable', safe=False)
        if ReviewColors.objects.filter(Q(score_from__gte=score_from, score_to__lte=score_to) | Q(color=color)).exists():
            return JsonResponse('not_available', safe=False)
        ReviewColors.objects.create(color=color, description=description, score_from=score_from, score_to=score_to)
        return JsonResponse('true', safe=False)

@login_required   
def colors(request):
    colors = ReviewColors.objects.all()
    color_dict = {}
    for x in colors:
        color_dict[x.color] = [x.description, x.score_to, x.score_from]
    context = {'color_dict' : color_dict}
    return render(request, 'coordinator/colors.html', context)
    
def logout(request):
    if is_logged_in(request):
        request.session.flush()
        return redirect(login)
    return redirect(login)