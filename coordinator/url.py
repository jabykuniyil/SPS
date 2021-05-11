from django.contrib import admin
from django.urls import path
from . import views
from . import context_processors


urlpatterns = [
    path('', views.coordinator, name = 'coordinator'),
    path('login/', views.login, name = 'coordinator-login'),
    path('search/', views.search, name = 'search'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('students/', views.students, name = 'students'),
    path('add-student/', views.add_student, name = 'add-student'),
    path('edit-student/', views.edit_student, name = 'edit-student'),
    path('students-requests/', views.students_requests, name = 'students-requests'),
    path('batches/', views.batches, name = 'batches'),
    path('batch-tasks/batch-specific/<str:name>/', views.batch_specific, name = 'batch-specific'),
    path('assign-week/<int:id>/', views.assign_week, name = 'assign-week'),
    path('edit-week-assign/<int:weekid>/<int:batchid>/', views.edit_week_assign, name = "edit-week-assign"),
    path('add-batch/', views.add_batch, name = 'add-batch'),
    path('student-specific/<int:id>/', views.student_specific, name = 'student-specific'),
    path('remove-suspension/<int:id>/', views.remove_suspension, name = 'remove-suspension'),
    path('terminate-student/<int:id>/', views.terminate_student, name = 'terminate-student'),
    path('remove-termination/<int:id>/', views.remove_termination, name = 'remove-termination'),
    path('student-placed/<int:id>/', views.student_placed, name = 'student-placed'),
    path('student-task/<int:weekid>/<int:studentid>/', views.student_task, name = 'student-task'),
    path('task-id/<int:id>/', views.task_id, name ='task-id'),
    path('student-review/<int:studentid>/<int:weekid>/', views.student_review, name = 'student-review'),
    path('edit-review/<int:studentId>/<int:week>/', views.edit_review, name = 'edit-review'),
    path('shift-batch/<int:id>/', views.shift_batch, name = 'shift-batch'),
    path('edit-answer/<int:taskid>/<int:studentid>/', views.edit_answer, name = 'edit-answer'),
    path('choose-week/', views.choose_week, name = 'choose-week'),
    path('add-week/', views.add_week, name = 'add-week'),
    path('task-specific/<int:weekid>/', views.task_specific, name = 'task-specific'),
    path('task-specific/<int:weekid>/delete-task/<int:taskid>/', views.delete_task, name = 'delete-task'),
    path('task-specific/<int:weekid>/edit-task/<int:taskid>/', views.edit_task, name = 'edit-task'),
    path('add-color/', views.add_color, name = 'add-color'),
    path('colors/', views.colors, name = 'colors'),
    path('logout/', views.logout, name = 'logout')
]