from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from . models import Student, CautionDeposit, EmailOTP, StudentUUID, InvalidResponse, VideocallShedule, Answer, Review
from django.urls import reverse
from . decorators import payment_required, student_status
from django.core.mail import send_mail
from django.core.files import File
from django.contrib import messages
from django.conf import settings
from coordinator.models import Week, Task, BatchSettings
import random, datetime

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect(feed)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password=password)
        if user is not None and user.is_superuser == False:
            if user.email_verfied == True:
                auth.login(request, user)
                if user.admin_approval == 'approved' and user.payment == True:
                    context = {'status' : 'true'}
                    return JsonResponse(context)
                elif user.admin_approval == 'rejected':
                    context = {'status' : 'login'}
                    return JsonResponse(context)
                student = request.user
                context = {'status' : 'wait-for-approval', 'id' : student.id}
                return JsonResponse(context)
            otp_email_generation(user)
            request.session['email'] = user.email
            context = {'status' : 'email'}
            return JsonResponse(context)
        context = {'status' : 'false'}
        return JsonResponse(context)
    return render(request, 'student/login.html')

@login_required(login_url='/')
@student_status
def payment(request):
    if request.method == 'POST':
        user = request.user
        if user.payment == False:
            payment_mode = request.POST['paymentMode']
            amount = 10000
            CautionDeposit.objects.create(payment_mode=payment_mode, amount=amount, student=user)
            user.payment = True
            user.save()
            return JsonResponse('true', safe=False)
        return JsonResponse('true', safe=False)
    return render(request, 'student/payment.html')
    
@login_required(login_url='/')
@payment_required
def dashboard(request):
    return render(request, 'student/dashboard.html')
    
def register(request):
    if request.user.is_authenticated:
        return redirect(feed)
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        phone = request.POST['phone']
        domain = request.POST['domain']
        age = request.POST['age']
        dob = request.POST['dob']
        father = request.POST['father']
        mother = request.POST['mother']
        address = request.POST['address']
        photo = request.FILES.get('photo')
        username = request.POST['username']
        password = request.POST['password']
        if Student.objects.filter(email=email).exists():
            return JsonResponse('email', safe=False)
        elif Student.objects.filter(username=username).exists():
            return JsonResponse('username', safe=False)
        elif Student.objects.filter(phone=phone).exists():
            return JsonResponse('phone', safe=False)
        student = Student.objects.create_user(fullname=fullname, email=email, phone=phone, domain=domain, age=age, dob=dob, father=father, mother=mother, address=address, photo=photo, username=username, password=password, admin_approval='pending')
        otp_email_generation(student)
        request.session['email'] = email
        return JsonResponse('true', safe=False)
    return render(request, 'student/register.html')
        
def verify_email(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.user.is_authenticated:
        return redirect(feed)
    if request.session.has_key('email'):
        if request.method == 'POST':
            otp = request.POST['otp']
            email = request.session['email']
            current_time = datetime.datetime.now()
            student =  Student.objects.filter(email=email).first()
            if student is not None:
                student_otp = EmailOTP.objects.filter(student=student, otp=otp).first()                
                if student_otp is not None:
                    f = '%Y-%m-%d %H:%M:%S'
                    otp_expiry_time = datetime.datetime.strptime(str(student_otp.otp_expiry).split('.')[0], f)
                    if otp_expiry_time > current_time:
                        student.email_verfied = True
                        student.save()
                        user = Student.objects.get(id=student.id)
                        student_otp.delete()
                        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        return redirect(wait_for_approval, id=user.id)
                    student_otp.delete()
                    messages.error(request, 'OTP expired')
                    return redirect(verify_email)
                messages.error(request, 'Invalid OTP')
                return redirect(verify_email)
            return redirect(register)
        return render(request, 'student/email-verification.html')
    return redirect(register)
        
def otp_email_generation(student):
    otp = random.randint(100000,999999)
    now = datetime.datetime.now()
    otp_expiry = now + datetime.timedelta(minutes = 5)
    EmailOTP.objects.create(student=student, otp=otp, otp_expiry=otp_expiry)
    send_mail("SPS login", "Your SPS login code is " + str(otp), "mohdjabiran112@gmail.com", [student.email])
    
def wait_for_approval(request, id):
    if request.user.is_authenticated:
        user = request.user
        if user.admin_approval == 'approved':
            return redirect(payment)
        elif user.admin_approval == 'rejected':
            return redirect(login)
        elif user.admin_approval == 'invalid':
            student = Student.objects.get(id=id)
            student_uuid = StudentUUID.objects.filter(student=student).first()
            context = {'student_uuid' : student_uuid.student_uuid}
            return render(request, 'student/waiting-for-approval.html', context)
        elif user.admin_approval == 'videocall':
            student = VideocallShedule.objects.get(student=user)
            date_and_time = str(student.date) + " " + str(student.time)
            context = {'datetime' : date_and_time}
            return render(request, 'student/waiting-for-approval.html', context)
        return render(request, 'student/waiting-for-approval.html')            
    return redirect(login)
    
@login_required(login_url='/')
def edit_registration(request, id):
    user = request.user
    student = Student.objects.get(id=user.id)
    if request.method == 'POST':
        student.fullname = request.POST['fullname']
        Student.objects.filter(phone=student.phone).delete()
        student.phone = request.POST['phone']
        student.domain = request.POST['domain']
        student.age = request.POST['age']
        student.dob = request.POST['dob']
        student.father = request.POST['father']
        student.mother = request.POST['mother']
        student.address = request.POST['address']
        student.photo = request.FILES.get('inputprofileimage')
        if Student.objects.filter(phone=student.phone).exists():
            return JsonResponse('phone', safe=False)
        student.save()
        request.session['email'] = student.email
        Student.objects.filter(admin_approval='invalid', id=user.id, is_superuser=False).update(admin_approval='pending')
        return JsonResponse('true', safe=False)
    invalid_reason = InvalidResponse.objects.filter(student=student).first()
    messages.error(request, invalid_reason.reason)
    student_context = StudentUUID.objects.filter(student=student, student_uuid=id).first()
    context = {'student' : student_context}
    return render(request, 'student/edit-registration.html', context)
        
@login_required(login_url='/')
@payment_required
@student_status
def feed(request):
    return render(request, 'student/feed.html')

@login_required(login_url='/')
@payment_required
@student_status
def profile(request):
    if request.method == 'POST':
        text = request.POST['text']
        print(text)
        return JsonResponse('true', safe=False)
    return render(request, 'student/profile.html')

@login_required(login_url='/')
@payment_required
@student_status
def choose_week(request):
    user = request.user
    student_batch = Student.objects.get(batch=user.batch)
    batches = BatchSettings.objects.filter(batch=student_batch.batch)
    weeks = []
    for x in batches:
        weeks.append(x.week)
    context = {'weeks' : weeks, 'id' : student_batch.batch.id}
    return render(request, 'student/choose-week.html', context)
    
@login_required(login_url='/')
@payment_required
@student_status
def task_specific(request, id):
    user = request.user
    if request.method == 'POST':
        answer = request.POST['answer']
        task_id = request.POST['taskid']
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Answer.objects.create(task_id=task_id, answer=answer, student=user, time=time, editor=user.username)
        return JsonResponse('true', safe=False)
    week = Week.objects.get(id=id)
    miscelleneous_task = Task.objects.filter(week=week, type_of_task='Miscelleneuos Task')
    personal_development = Task.objects.filter(week=week, type_of_task='Personal Development')
    technical_task = Task.objects.filter(week=week, type_of_task='Technical Task')
    miscelleneous_task_dict = {}
    personal_development_dict = {}
    technical_task_dict = {}
    student_answers = Answer.objects.filter(student=user)
    time = datetime.datetime.now()
    largest = datetime.datetime(2000,12,2,12,32,21)
    for x in student_answers:
        answer_time = datetime.datetime.strptime(x.time, '%Y-%m-%d %H:%M:%S')
        if answer_time > largest:
            largest = answer_time
    editor = Answer.objects.get(time=largest)
    evaluated = time - largest
    time_dict = {}
    time_dict['days'] = evaluated.days
    time_dict['hours'] = evaluated.seconds//3600
    time_dict['minutes'] = (evaluated.seconds//60)%60
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
        'time_dict' : time_dict,
        'editor' : editor
        }
    return render(request, 'student/task-specific.html', context)
    
@login_required(login_url='/')
@payment_required
@student_status
def edit_answer(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        answer = request.POST['answer']
        student = request.user
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Answer.objects.filter(task=task, student=student).update(answer=answer, student=student, time=time, editor=student.username)
        return JsonResponse('true', safe=False)
    
@login_required(login_url='/')
@payment_required
@student_status
def delete_answer(request, id):
    answer = Answer.objects.get(task_id=id)
    answer.delete()
    return redirect(choose_week)  

@login_required(login_url='/')
@payment_required
@student_status
def review(request):
    review = Review.objects.filter(student_id=request.user.id)
    week_list = []
    for x in review:
        week_list.append(x)
    context = {'weeks' : week_list}
    return render(request, 'student/review.html', context)  
    
@login_required(login_url='/')
@payment_required
@student_status
def logout(request):
    user = request.user
    auth.logout(request)
    return redirect(login)