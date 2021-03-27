from django.db import models
from coordinator.models import CoordinatorDetails
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Student(AbstractUser):
    payment = models.BooleanField(default=False)
    fullname = models.CharField(max_length=30, null=True, blank=True)
    phone = models.BigIntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    batch = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=30, null=True, blank=True)
    father = models.CharField(max_length=30, null=True, blank=True)
    mother = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    domain = models.CharField(max_length=30, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    email_verfied = models.BooleanField(default=False)
    admin_approval = models.CharField(max_length=20, null=True, blank=True)
    
    @property
    def student_photo(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url
    
class EmailOTP(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    otp = models.IntegerField(null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    
class CautionDeposit(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True) 
    amount = models.IntegerField(null=True, blank=True)
    payment_mode = models.CharField(max_length=20, null=True, blank=True)
    
class InvalidResponse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200, null=True, blank=True)
    
class StudentUUID(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_uuid = models.CharField(max_length=50, null=True, blank=True)
    uuid_expiry = models.DateField(null=True, blank=True)
    