from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name = 'coordinator-login'),
    path('feed/', views.feed, name = 'feed'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('profile/', views.profile, name = 'profile'),
    path('students/', views.students, name = 'students'),
    path('add-student/', views.add_student, name = 'add-student'),
    path('edit-student/', views.edit_student, name = 'edit-student'),
    path('students-requests/', views.students_requests, name = 'students-requests'),
    path('batches/', views.batches, name = 'batches'),
    path('batch-specific/', views.batch_specific, name = 'batch-specific'),
    path('add-batch/', views.add_batch, name = 'add-batch'),
    path('batch-tasks/', views.batch_tasks, name = 'batch-tasks'),
    path('choose-week/<int:id>/', views.choose_week, name = 'choose-week'),
    path('add-week/<int:id>/', views.add_week, name = 'add-week'),
    path('<int:batchid>/task-specific/<int:weekid>/', views.task_specific, name = 'task-specific'),
    path('<int:batchid>/task-specific/<int:weekid>/delete-task/<int:taskid>/', views.delete_task, name = 'delete-task'),
    path('<int:batchid>/task-specific/<int:weekid>/edit-task/<int:taskid>/', views.edit_task, name = 'edit-task'),
    path('logout/', views.logout, name = 'logout')
]