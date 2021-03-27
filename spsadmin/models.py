from django.db import models

# Create your models here.

class AdminProfile(models.Model):
    phone = models.BigIntegerField()
    photo = models.ImageField()
    email = models.EmailField()
    name = models.CharField(max_length=30)