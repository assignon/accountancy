from django.db import models

# Create your models here.

class WareHouse(models.Model):
    items_id = models.IntegerField()
    items_name = models.CharField(max_length=255)
    quantity_available = models.IntegerField()
    limit_price = models.IntegerField()
    quantity_sold = models.IntegerField()
    pay_choices = (('cash', 'cash'), ('credit', 'credit'))
    payment = models.CharField(max_length=255, choices=pay_choices, default='cash')
    customer_name = models.CharField(max_length=255)
    customer_number = models.IntegerField()
    city = models.CharField(max_length=255)
