from statistics import mode
from django.db import models

class Invoice(models.Model):
    name = models.CharField(max_length=255)
    rfc = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    outdoor_number = models.IntegerField()
    interior_number = models.CharField(max_length=255, default='1')
    suburb = models.CharField(max_length=255)
    cp = models.BigIntegerField()
    municipality = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    email = models.EmailField()
    cell_phone_number = models.BigIntegerField()
    way_pay = models.CharField(max_length=255)
    bill_usage = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name