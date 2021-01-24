from django.db import models
from products.models import Tires
from datetime import datetime, timedelta
from calendar import monthrange
from .managers import *

# Create your models here.


class PaymentMethods(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Payment(models.Model):
    method = models.ForeignKey(PaymentMethods, on_delete=models.CASCADE)
    pay_choices = (('once', 'once'), ('terms', 'terms'))
    pay_in = models.CharField(
        max_length=50, choices=pay_choices, default='once')
    pay_interval = (('daily', 'daily'), ('weekly', 'weekly'),
                    ('monthly', 'monthly'))
    payment_interval = models.CharField(
        max_length=50, choices=pay_interval, default='daily')
    times = models.IntegerField()
    start = models.DateField()
    objects = PaymentManager()

    @staticmethod
    def paymentDates_end(id):
        # payment end date of payment and dates of payments
        self = Payment.objects.get(id=id)
        # -1 because the 1st payment happen on the order day
        times = self.times-1
        order_date = datetime.now().date()
        payment_dates = []

        if self.pay_in == 'once':
            return self.start
        else:
            if self.payment_interval == 'daily':
                for count in range(self.times):
                    payment_dates.append(self.start + timedelta(days=count))

                end_date = self.start + timedelta(days=times)

                return {'paying_dates': payment_dates, 'end': end_date}
            elif self.payment_interval == 'weekly':
                for count in range(self.times):
                    payment_dates.append(self.start + timedelta(days=count*7))

                end_date = self.start + timedelta(days=times*7)

                return {'paying_dates': payment_dates, 'end': end_date}
            else:
                # get number of days in current month(moth order take place)
                days_in_month = monthrange(
                    order_date.year, order_date.month)[0]

                for count in range(self.times):
                    payment_dates.append(
                        self.start + timedelta(days=count*days_in_month))

                end_date = self.start + timedelta(days=times*days_in_month)

                # return {'paying_dates': payment_dates, 'end': end_date}
                return end_date

    @staticmethod
    def paying_in_terms(id):
        self = Payment.objects.get(id=id)
        if self.pay_in == 'terms':
            return int(Orders.paying(id))/int(self.times)

    @staticmethod
    def completed(id):
        if Payment.paymentDates_end(id)['end'] == datetime.now().date():
            return True
        else:
            return False

    def __str__(self):
        return PaymentMethods.objects.get(id=self.method_id).name


class Orders(models.Model):
    product = models.ManyToManyField(Tires)
    quantity = models.IntegerField()
    order_on = models.DateField(auto_now=True)
    order_at = models.TimeField(auto_now=True)
    objects = OrdersManager()

    class Meta:
        ordering = ['-id']

    @staticmethod
    def total(dte=None):
        if dte == None:
            return Orders.objects.filter(order_on=datetime.now().date())
        else:
            return Orders.objects.filter(order_on=dte)

    @staticmethod
    def paying(id):
        self = Orders.objects.get(id=id)
        total_price = 0
        products = self.product.all().values()
        for product in products:
            total_price += product['price']

        return total_price


class Credentials(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    tel_number = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Customers(models.Model):
    credential = models.ForeignKey(Credentials, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING)
    objects = CustomerManager()

    @staticmethod
    def total():
        return Customers.objects.all().count()

    def __str__(self):
        return Credentials.objects.get(id=self.credential_id).name
