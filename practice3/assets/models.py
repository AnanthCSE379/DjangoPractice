from django.db import models
from django.core.validators import MinValueValidator


class Asset(models.Model):
    asset_id = models.CharField(max_length=20,unique=True)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=30)
    purchase_date = models.DateField()
    cost = models.DecimalField(max_digits=10,decimal_places=2,
                               validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20,choices=[
        ('Active','Active'), ('Decommissioned','Decommissioned')
    ])
    location = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
