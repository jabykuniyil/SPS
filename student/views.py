from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from . models import Student, CautionDeposit, EmailOTP, StudentUUID
from django.urls import reverse
from . decorators import payment_required, student_status
from django.core.mail import send_mail
from django.core.files import File
import random
from django.contrib import messages
import datetime
from django.conf import settings

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
                        return JsonResponse('true', safe=False)
                    elif user.admin_approval == 'rejected':
                        return JsonResponse('login')
                    else:
                        return JsonResponse('wait-for-approval', safe=False)
                else:
                    otp_email_generation(user)
                    request.session['email'] = user.email
                    return JsonResponse('email', safe=False)
            else:
                return JsonResponse('false', safe=False)
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
                            return redirect(wait_for_approval)
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
        else:
            return render(request, 'student/waiting-for-approval.html')            
    else:
        return redirect(login)
    
@login_required(login_url='/')
def edit_registration(request, id):
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
        user = request.user
        student = Student.objects.get(id=user.id)
        student_uuid = StudentUUID.objects.get(student=student, student_uuid=id)
        context = {'student_uuid' : student_uuid}
        return render(request, 'student/edit-registration.html', context)
        
@login_required(login_url='/')
@payment_required
@student_status
def feed(request):
    return render(request, 'student/feed.html')
    
@login_required(login_url='/')
@payment_required
@student_status
def logout(request):
    user = request.user
    auth.logout(request)
    return redirect(login)