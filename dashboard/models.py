from django.db import models
from django.db.models.fields import CharField

# Create your models here.


# class WareHouse(models.Model):
#     items_id = models.IntegerField()
#     items_name = models.CharField(max_length=255)
#     quantity_available = models.IntegerField()
#     limit_price = models.IntegerField()
#     quantity_sold = models.IntegerField()
#     pay_choices = (('cash', 'cash'), ('credit', 'credit'))
#     payment = models.CharField(
#         max_length=255, choices=pay_choices, default='cash')
#     customer_name = models.CharField(max_length=255)
#     customer_number = models.IntegerField()
#     city = models.CharField(max_length=255)


class Brands(models.Model):
    name = models.CharField(max_length=255)


class Vehicule(models.Model):
    name = models.CharField(max_length=100)


class Tires(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brands = models.ManyToManyField(Brands)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.DO_NOTHING)


class Products(models.Model):
    tire = models.ForeignKey(Tires, on_delete=models.DO_NOTHING)
    add_on = models.DateTimeField(auto_now=True)


class PaymentMethods(models.Model):
    name = models.CharField(max_length=100)


class Payment(models.Model):
    method = models.ForeignKey(PaymentMethods, on_delete=models.CASCADE)
    pay_choices = (('once', 'once'), ('terms', 'terms'))
    pay_in = models.CharField(
        max_length=50, choices=pay_choices, default='once')
    pay_interval = (('daily', 'daily'), ('weekly', 'weekly'),
                    ('monthly', 'monthly'))
    payment_interval = models.CharField(
        max_length=50, choices=pay_interval, default='once')
    times = models.IntegerField()


class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now=True)


class Credentials(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    tel_number = models.CharField(max_length=50)


class Customers(models.Model):
    credential = models.ForeignKey(Credentials, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING)
