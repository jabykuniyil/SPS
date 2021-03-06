from django.db import models
from colorfield.fields import ColorField

# Create your models here.

class CoordinatorDetails(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.BigIntegerField( null=True, blank=True)
    address = models.TextField( null=True, blank=True)
    age = models.IntegerField( null=True, blank=True)
    dob = models.DateField( null=True, blank=True)
    salary = models.BigIntegerField( null=True, blank=True)
    education = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    father = models.CharField(max_length=30, null=True, blank=True)
    mother = models.CharField(max_length=30, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True)
    password = models.TextField( null=True, blank=True)
    status = models.CharField(null=True, blank=True, max_length=20)
    
    @property
    def ImageURL(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url
    
class Batches(models.Model):
    name = models.CharField(null=True, blank=True, max_length=20)
    capacity = models.IntegerField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    
class Week(models.Model):
    week = models.IntegerField(null=True, blank=True)
    batch = models.ForeignKey(Batches, on_delete=models.CASCADE, null=True, blank=True)
    
class Task(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    question = models.TextField(null=True, blank=True)
    type_of_task = models.CharField(null=True, blank=True, max_length=30)
    
class BatchSettings(models.Model):
    batch = models.ForeignKey(Batches, on_delete=models.CASCADE)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    
class ReviewColors(models.Model):
    color = ColorField()
    description = models.CharField(max_length=20, null=True, blank=True)
    score_from = models.IntegerField(null=True, blank=True)
    score_to = models.IntegerField(null=True, blank=True)