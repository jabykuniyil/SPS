from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests, json
from django.contrib.auth.models import auth, User
from coordinator.models import CoordinatorDetails
from django.core.files import File
from django.contrib.auth.hashers import make_password
from student.models import Student, InvalidResponse, StudentUUID
from coordinator.models import Batches
from django.contrib.auth.decorators import login_required
import uuid
import datetime

# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect(feed)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                if user.is_superuser == True:
                    auth.login(request, user)
                    return JsonResponse('true', safe = False)
            else:
                return JsonResponse('false', safe = False)
        return render(request, 'admin/login.html')

@login_required(login_url='/spsadmin/')
def phone(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        if phone == '8547494184':
            request.session['phone'] = phone
            url = "https://d7networks.com/api/verifier/send"
            phone_str = '91' + str(phone)
            payload = {'mobile' : phone_str,
                        'sender_id' : 'SMSINFO',
                        'message' : 'Your SPS verification code is {code}',
                        'expiry' : '900'}
            files = [
                
            ]
            headers = {
            'Authorization': 'Token 0826e09c83c02826d9767d57fed74ead46c7660a'
            }
            response = requests.request('POST', url, headers=headers, data = payload, files = files)
            data = response.text.encode('utf8')
            dict = json.loads(data.decode('utf8'))
            otp_id = dict['otp_id']
            request.session['otp_id'] = otp_id
            return JsonResponse('true', safe = False)
        else:
            return JsonResponse('false', safe = False)
    else:
        return render(request, 'admin/phone.html')
        
@login_required(login_url='/spsadmin/')
def otp(request):
    if request.method == 'POST':
        phone = request.session['phone']
        url = "https://d7networks.com/api/verifier/verify"
        otp = request.POST['otp']
        otp_id = request.session['otp_id']
        payload = {'otp_id' : otp_id, 'otp_code' : otp}
        files = [
            
        ]
        headers = {
        'Authorization': 'Token 0826e09c83c02826d9767d57fed74ead46c7660a'
        }
        response = requests.request('POST', url, headers = headers, data = payload, files = files)
        data = response.text.encode('utf8')
        dict = json.loads(data.decode('utf8'))
        status = dict['status']
        if status == 'success':
            return JsonResponse('true', safe = False)
        else:
            return JsonResponse('false', safe = False)
    else:
        if request.session.has_key('otp_id'):
            return render(request, 'admin/otp.html')
        else:
            return redirect(login)
        
@login_required(login_url='/spsadmin/')
def feed(request):
    return render(request, 'admin/feed.html')

@login_required(login_url='/spsadmin/')
def profile(request):
    return render(request, 'admin/profile.html')

@login_required(login_url='/spsadmin/')
def dashboard(request):
    return render(request, 'admin/dashboard.html')

@login_required(login_url='/spsadmin/')
def students_placed(request):
    return render(request, 'admin/students-placed.html')

@login_required(login_url='/spsadmin/')
def students(request):
    students = Student.objects.filter(is_superuser=False, admin_approval='approved')
    context = {'students' : students}
    return render(request, 'admin/students.html', context)

@login_required(login_url='/spsadmin/')
def student_register(request):
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
        return render(request, 'admin/student-register.html', context)

@login_required(login_url='/spsadmin/')
def students_requests(request):
    students = Student.objects.filter(admin_approval='pending', is_superuser=False)
    context = {'students' : students}
    return render(request, 'admin/students-requests.html', context)

@login_required(login_url='/spsadmin/')
def invalid_student_requests(request):
    students = Student.objects.filter(admin_approval='invalid', is_superuser=False)
    context = {'students' : students}
    return render(request, 'admin/invalid-requests.html', context)

@login_required(login_url='/spsadmin/')
def student_specific(request, id):
    student = Student.objects.get(id=id)
    context = {'student' : student}
    return render(request, 'admin/student-specific.html', context)
    
@login_required(login_url='/spsadmin/')
def approve_student(request, id):
    Student.objects.filter(admin_approval__in=['pending', 'terminated', 'rejected'], id=id, is_superuser=False).update(admin_approval='approved')
    return redirect(students)

@login_required(login_url='/spsadmin/')
def reject_student(request, id):
    Student.objects.filter(id=id, admin_approval='pending', is_superuser=False).update(admin_approval='rejected')
    return redirect(students)

@login_required(login_url='/spsadmin/')
def invalid_request(request, id):
    if request.method == 'POST':
        reason = request.POST['reason']
        student = Student.objects.get(id=id)
        InvalidResponse.objects.create(student=student, reason=reason)
        Student.objects.filter(admin_approval='pending', id=id, is_superuser=False).update(admin_approval='invalid')
        student_uuid  = uuid.uuid4()
        print(student_uuid)
        today = datetime.datetime.now().date()
        print(today)
        uuid_expiry = today + datetime.timedelta(days=1)
        print(uuid_expiry)
        StudentUUID.objects.create(student=student, student_uuid=student_uuid, uuid_expiry=uuid_expiry)
        return JsonResponse('true', safe=False)
    else:
        return JsonResponse('true', safe=False)
    
@login_required(login_url='/spsadmin/')
def terminate_student(request, id):
    Student.objects.filter(id=id, admin_approval='approved', is_superuser=False).update(admin_approval='terminated')
    return redirect(students)

@login_required(login_url='/spsadmin/')
def rejected_requests(request):
    students = Student.objects.filter(admin_approval='rejected', is_superuser=False)
    context = {'students' : students}
    return render(request, 'admin/rejected-requests.html', context)
    
def staffs(request):
    coordinator_details = CoordinatorDetails.objects.all()
    context = {'coordinator_details' : coordinator_details}
    return render(request, 'admin/staffs.html', context)
    
@login_required(login_url='/spsadmin/')
def staff_register(request):
    if request.method == 'POST':
        name = request.POST['fullname']
        email = request.POST['email']
        phone = request.POST['phone']
        salary = request.POST['salary']
        age = request.POST['age']
        dob = request.POST['dob']
        gender = request.POST['gender']
        father = request.POST['father']
        mother = request.POST['mother']
        education = request.POST['education']
        address = request.POST['address']
        photo = request.FILES.get('photo')
        username = request.POST['username']
        password = request.POST['password']
        if CoordinatorDetails.objects.filter(username=username).exists():
            return JsonResponse('username', safe=False)
        elif CoordinatorDetails.objects.filter(email=email).exists():
            return JsonResponse('email', safe=False)
        else:
            CoordinatorDetails.objects.create(name=name, email=email, phone=phone, salary=salary, age=age, dob=dob, gender=gender, father=father, mother=mother, address=address, education=education, photo=photo, username=username, password=make_password(password))
            return JsonResponse('true', safe=False)
    else:
        return render(request, 'admin/staff-register.html')

@login_required(login_url='/spsadmin/')
def edit_coordinator(request, id):
    if request.method == 'POST':
        coordinator_details = CoordinatorDetails.objects.get(id=id)
        coordinator_details.name = request.POST['fullname']
        coordinator_details.email = request.POST['email']
        coordinator_details.phone = request.POST['phone']
        coordinator_details.age = request.POST['age']
        coordinator_details.salary = request.POST['salary']
        coordinator_details.father = request.POST['father']
        coordinator_details.mother = request.POST['mother']
        coordinator_details.address = request.POST['address']
        coordinator_details.education = request.POST['education']
        coordinator_details.gender = request.POST['gender']
        coordinator_details.save()
        return JsonResponse('true', safe=False)
    else:
        coordinator_details = CoordinatorDetails.objects.get(id=id)
        context = {'coordinator_details' : coordinator_details}
        return render(request, 'admin/edit-coordinator.html', context)

@login_required(login_url='/spsadmin/')
def delete_coordinator(request, id):
    coordinator_details = CoordinatorDetails.objects.get(id=id)
    coordinator_details.delete()
    return redirect(staffs)
   
@login_required(login_url='/spsadmin/')
def host_meeting(request):
    return render(request, 'admin/host-meeting.html')

@login_required(login_url='/spsadmin/')
def branches(request):
    return render(request, 'admin/branches.html')

@login_required(login_url='/spsadmin/')
def logout(request):
    auth.logout(request)
    return redirect(login)
    
@login_required(login_url='/spsadmin/')
def tasks(request):
    coordinator_details = CoordinatorDetails.objects.all()
    context = {'count' : coordinator_details}
    return render(request, 'admin/tasks.html', context)