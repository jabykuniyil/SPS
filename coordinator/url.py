from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login, name = 'coordinator-login'),
    path('feed/', views.feed, name = 'feed'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('profile/', views.profile, name = 'profile'),
    path('students/', views.students, name = 'students'),
    path('add-student/', views.add_student, name = 'add-student'),
    path('edit-student/', views.edit_student, name = 'edit-student'),
    path('students-requests/', views.students_requests, name = 'students-requests'),
    path('batches/', views.batches, name = 'batches'),
    path('batch-tasks/batch-specific/<str:name>/', views.batch_specific, name = 'batch-specific'),
    path('assign-week/<int:id>/', views.assign_week, name = 'assign-week'),
    path('add-batch/', views.add_batch, name = 'add-batch'),
    path('student-specific/<int:id>/', views.student_specific, name = 'student-specific'),
    path('student-task/<int:weekid>/<int:studentid>/', views.student_task, name = 'student-task'),
    path('edit-answer/<int:taskid>/<int:studentid>/', views.edit_answer, name = 'edit-answer'),
    path('choose-week/', views.choose_week, name = 'choose-week'),
    path('add-week/', views.add_week, name = 'add-week'),
    path('task-specific/<int:weekid>/', views.task_specific, name = 'task-specific'),
    path('task-specific/<int:weekid>/delete-task/<int:taskid>/', views.delete_task, name = 'delete-task'),
    path('task-specific/<int:weekid>/edit-task/<int:taskid>/', views.edit_task, name = 'edit-task'),
    path('add-color/', views.add_color, name = 'add-color'),
    path('review/', views.review, name = 'review'),
    path('logout/', views.logout, name = 'logout')
]