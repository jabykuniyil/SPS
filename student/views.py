from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from . models import Student, CautionDeposit, EmailOTP, StudentUUID, InvalidResponse, VideocallShedule
from django.urls import reverse
from . decorators import payment_required, student_status
from django.core.mail import send_mail
from django.core.files import File
import random
from django.contrib import messages
import datetime
from django.conf import settings
from coordinator.models import Week, Task

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect(feed)
    else:
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
                    else:
                        student = request.user
                        context = {'status' : 'wait-for-approval', 'id' : student.id}
                        return JsonResponse(context)
                else:
                    otp_email_generation(user)
                    request.session['email'] = user.email
                    context = {'status' : 'email'}
                    return JsonResponse(context)
            else:
                context = {'status' : 'false'}
                return JsonResponse(context)
        else:
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
        else:
            return JsonResponse('true', safe=False)
    else:
        return render(request, 'student/payment.html')
    
@login_required(login_url='/')
@payment_required
def dashboard(request):
    return render(request, 'student/dashboard.html')
    
def register(request):
    if request.user.is_authenticated:
        return redirect(feed)
    else:
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
            else:
                student = Student.objects.create_user(fullname=fullname, email=email, phone=phone, domain=domain, age=age, dob=dob, father=father, mother=mother, address=address, photo=photo, username=username, password=password, admin_approval='pending')
                otp_email_generation(student)
                request.session['email'] = email
                return JsonResponse('true', safe=False)
        else:
            return render(request, 'student/register.html')
        
def verify_email(request, backend='django.contrib.auth.backends.ModelBackend'):
    if request.user.is_authenticated:
        return redirect(feed)
    else:
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
                        else:
                            student_otp.delete()
                            messages.error(request, 'OTP expired')
                            return redirect(verify_email)
                    else:
                        messages.error(request, 'Invalid OTP')
                        return redirect(verify_email)
                else:
                    return redirect(register)
            else:
                return render(request, 'student/email-verification.html')
        else:
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
        else:
            return render(request, 'student/waiting-for-approval.html')            
    else:
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
        else:
            student.save()
            request.session['email'] = student.email
            Student.objects.filter(admin_approval='invalid', id=user.id, is_superuser=False).update(admin_approval='pending')
            return JsonResponse('true', safe=False)
    else:
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
def choose_week(request):
    weeks = Week.objects.all()
    context = {'weeks' : weeks}
    return render(request, 'student/choose-week.html', context)
    
@login_required(login_url='/')
@payment_required
@student_status
def task_specific(request, id):
    if request.method == 'POST':
        answer = request.POST['answer']
        type_of_task = request.POST['type']
        Task.objects.filter(id=id, type_of_task=type_of_task).update(answer=answer)
        return JsonResponse('true', safe=False)
    else:
        week = Week.objects.get(id=id)
        miscelleneous_task = Task.objects.filter(week=week, type_of_task='Miscelleneuos Task')
        personal_development = Task.objects.filter(week=week, type_of_task='Personal Development')
        technical_task = Task.objects.filter(week=week, type_of_task='Technical Task')
        miscelleneous_task_dict = {}
        personal_development_dict = {}
        technical_task_dict = {}
        miscelleneous_answers = []
        technical_answers = []
        personal_answers = []
        for x in technical_task:
            technical_task_dict[x.id] = x.question
        for x in miscelleneous_task:
            miscelleneous_task_dict[x.id] = x.question
        for x in personal_development:
            personal_development_dict[x.id] = x.question
        for x in miscelleneous_task:
            miscelleneous_answers.append(x.answer)
        for x in technical_task:
            technical_answers.append(x.answer)
        for x in personal_development:
            personal_answers.append(x.answer)
        context = {'personal_tasks' : personal_development_dict, 'technical_tasks' : technical_task_dict, 'miscelleneous_tasks' : miscelleneous_task_dict, 'personal_answers' : personal_answers, 'technical_answers' : technical_answers, 'miscelleneous_answers' : miscelleneous_answers}
        return render(request, 'student/task-specific.html', context)
    
@login_required(login_url='/')
@payment_required
@student_status
def logout(request):
    user = request.user
    auth.logout(request)
    return redirect(login)