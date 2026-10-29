from django.db import models

# Create your models here.

class StaffPersonal(models.Model):
    staffid = models.IntegerField()
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    mobile = models.CharField(max_length=10)
    mail = models.CharField(max_length=20)
    dept = models.CharField(max_length=20)
