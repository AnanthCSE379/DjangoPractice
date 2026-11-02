from django.db import models

# Create your models here.

class Patient(models.Model):
    patientid = models.IntegerField(unique=True)
    name = models.CharField(max_length=30)
    admit_date = models.DateField()
    discharge_date = models.DateField()
    total_days = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
