from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name = 'admin-login'),
    path('phone/', views.phone, name = 'phone'),
    path('feed/', views.feed, name = 'admin-feed'),
    path('profile/', views.profile, name = 'profile'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('students-placed/', views.students_placed, name = 'students-placed'),
    path('students/', views.students, name = 'students'),
    path('staffs/', views.staffs, name = 'staffs'),
    path('edit-coordinator/<int:id>/', views.edit_coordinator, name = 'edit-coordinator'),
    path('delete-coordinator/<int:id>/', views.delete_coordinator, name = 'delete-coordinator'),
    path('staff-register/', views.staff_register, name = 'staff-register'),
    path('students-requests/', views.students_requests, name = 'students-requests'),
    path('student-specific/<int:id>/', views.student_specific, name = 'student-specific'),
    path('approve-student/<int:id>/', views.approve_student, name = 'approve-student'),
    path('reject-student/<int:id>/', views.reject_student, name = 'reject-student'),
    path('invalid-request/<int:id>/', views.invalid_request, name = 'invalid-request'),
    path('terminate-student/<int:id>/', views.terminate_student, name = 'terminate-student'),    
    path('rejected-requests/', views.rejected_requests, name = 'rejected-requests'),
    path('invalid-students-requests/', views.invalid_student_requests, name = 'invalid-students-requests'),
    path('host-meeting/', views.host_meeting, name = 'host-meeting'),
    path('branches/', views.branches, name = 'branches'),
    path('student-register/', views.student_register, name = 'student-register'),
    path('logout/', views.logout, name = 'logout'),
    path('tasks/', views.tasks, name = 'tasks'),
]