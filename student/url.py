from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name= 'student-login'),
    path('payment/', views.payment, name = 'student-payment'),
    path('register/', views.register, name = 'student-register'),
    path('verify-email/', views.verify_email, name = 'verify-email'),
    path('wait-for-approval/<int:id>/', views.wait_for_approval, name = 'wait-for-approval'),
    path('edit-registration/<int:id>/', views.edit_registration, name = 'edit-registration'),
    path('feed/', views.feed, name = 'student-feed'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('logout/', views.logout, name = 'logout')
]