from statistics import mode
from django.db import models

class Invoice(models.Model):
    name = models.CharField(max_length=50)
    rfc = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    outdoor_number = models.IntegerField()
    interior_number = models.IntegerField(null=True, blank=True, default=0)
    suburb = models.CharField(max_length=100)
    cp = models.BigIntegerField()
    municipality = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    email = models.EmailField()
    cell_phone_number = models.BigIntegerField()
    way_pay = models.CharField(max_length=100)
    bill_usage = models.CharField(max_length=250)
    
    def __str__(self) -> str:
        return self.name