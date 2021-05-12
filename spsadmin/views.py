from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import auth, User
from coordinator.models import CoordinatorDetails
from django.core.files import File
from django.contrib.auth.hashers import make_password
from student.models import Student, InvalidResponse, StudentUUID, VideocallShedule, Review
from coordinator.models import Batches, BatchSettings
from django.contrib.auth.decorators import login_required
from django.core import serializers
import uuid, datetime, requests, json

# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect(dashboard)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            if user.is_superuser == True:
                auth.login(request, user)
                return JsonResponse('true', safe = False)
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
        return JsonResponse('false', safe = False)
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
        return JsonResponse('false', safe = False)
    if request.session.has_key('otp_id'):
        return render(request, 'admin/otp.html')
    return redirect(login)

@login_required(login_url='/spsadmin/')
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

@login_required(login_url='/spsadmin/')
def dashboard(request):
    students = Student.objects.filter(is_superuser=False)
    staffs = CoordinatorDetails.objects.all()
    batches = Batches.objects.all()
    context = {'coordinators' : staffs, 'students' : students, 'batches' : batches}
    return render(request, 'admin/dashboard.html', context)

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
        Student.objects.create_user(fullname=fullname, email=email, phone=phone, batch__name=batch, age=age, dob=dob, gender=gender, address=address, father=father, mother=mother, domain=domain, photo=photo, username=username, password=password, payment=False, admin_approval='approved')
        return JsonResponse('true', safe=False)
    batches = Batches.objects.all()
    context = {'batches' : batches}
    return render(request, 'admin/student-register.html', context)

@login_required(login_url='/spsadmin/')
def students_requests(request):
    students = Student.objects.filter(admin_approval='pending', is_superuser=False)
    today = datetime.date.today()
    formated = datetime.date.strftime(today, '%Y-%m-%d')
    batches = Batches.objects.all()
    context = {'students' : students, 'today' : formated, 'batches' : batches}
    return render(request, 'admin/students-requests.html', context)

@login_required(login_url='/spsadmin/')
def invalid_student_requests(request):
    students = Student.objects.filter(admin_approval='invalid', is_superuser=False)
    batches = Batches.objects.all()
    context = {'students' : students, 'batches' : batches}
    return render(request, 'admin/invalid-requests.html', context)

@login_required(login_url='/spsadmin/')
def student_specific(request, id):
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
    context = {'student' : student, 'weeks' : weeks, 'review' : review}
    return render(request, 'admin/student-specific.html', context)
    
@login_required(login_url='/spsadmin/')
def approve_student(request, id):
    if request.method == 'POST':
        batch = request.POST['batch']
        batch = Batches.objects.get(name=batch)
        Student.objects.filter(admin_approval__in=['pending', 'terminated', 'rejected'], id=id, is_superuser=False).update(admin_approval='approved', batch=batch)
        return JsonResponse('true', safe=False)
    return JsonResponse('true', safe=False)

@login_required(login_url='/spsadmin/')
def approve_videocall(request, id):
    if request.method == 'POST':
        student = Student.objects.get(id=id)
        date = request.POST['date']
        time = request.POST['time']
        Student.objects.filter(id=id, admin_approval='pending').update(admin_approval='videocall')
        VideocallShedule.objects.create(student=student, date=date, time=time)
        return JsonResponse('true', safe=False)
    return JsonResponse('true', safe=False)

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
        today = datetime.datetime.now().date()
        uuid_expiry = today + datetime.timedelta(days=1)
        StudentUUID.objects.create(student=student, student_uuid=student_uuid, uuid_expiry=uuid_expiry)
        return JsonResponse('true', safe=False)
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

@login_required(login_url='/spsadmin/')
def student_videocall(request):
    if request.method == 'POST':
        id = request.POST['id']
        batch = request.POST['batch']
        Student.objects.filter(admin_approval='videocall', id = id).update(admin_approval='approved', batch=batch)
        return JsonResponse('true', safe=False)
    pending_students = VideocallShedule.objects.filter(student__admin_approval='videocall')
    schedule_list = {}
    for student in pending_students:
        videocall_date = str(student.date)
        videocall_time = str(student.time)
        date_and_time = videocall_date +" "+ videocall_time
        schedule_list[student.student.id] = date_and_time
    batches = Batches.objects.all()
    context = {'students' : pending_students, 'schedules' : schedule_list, 'batches' : batches}
    return render(request, 'admin/student-videocall.html', context)

@login_required(login_url='/spsadmin/')
def students_placed(request):
    students = Student.objects.filter(admin_approval='placed')
    context = {'students' : students}
    return render(request, 'admin/students-placed.html', context)
    
@login_required(login_url='/spsadmin/')
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
        CoordinatorDetails.objects.create(name=name, email=email, phone=phone, salary=salary, age=age, dob=dob, gender=gender, father=father, mother=mother, address=address, education=education, photo=photo, username=username, password=make_password(password))
        return JsonResponse('true', safe=False)
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
    coordinator_details = CoordinatorDetails.objects.get(id=id)
    context = {'coordinator_details' : coordinator_details}
    return render(request, 'admin/edit-coordinator.html', context)

@login_required(login_url='/spsadmin/')
def delete_coordinator(request, id):
    coordinator_details = CoordinatorDetails.objects.get(id=id)
    coordinator_details.delete()
    return redirect(staffs)

@login_required(login_url='/spsadmin/')
def coordinator_specific(request, id):
    coordinator = CoordinatorDetails.objects.get(id=id)
    context = {'coordinator' : coordinator}
    return render(request, 'admin/coordinator-specific.html', context)

@login_required(login_url='/spsadmin/')
def suspend_coordinator(request, id):
    CoordinatorDetails.objects.filter(id=id).update(status='suspended')
    return redirect(coordinator_specific, id)

@login_required(login_url='/spsadmin/')
def logout(request):
    auth.logout(request)
    return redirect(login)