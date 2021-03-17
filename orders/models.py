from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from products.models import Tires
from datetime import datetime, timedelta
from calendar import monthrange
from .managers import *

# Create your models here.


class PaymentMethods(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # avoid duplacate
        if PaymentMethods.objects.filter(name=self.name).count() > 0:
            raise Exception('This payment method already exists')
        return super().save(*args, **kwargs)


class Payment_status(models.Model):
    # track the customer payments status
    payment_date = models.DateField()
    payed = models.BooleanField(default=False)
    employee_name = models.CharField(
        max_length=200, default=None, blank=True, null=True)  # employee who receive the paymanet

    def __str__(self):
        pass


class Payment(models.Model):
    method = models.ForeignKey(PaymentMethods, on_delete=models.DO_NOTHING)
    pay_choices = (('once', 'once'), ('terms', 'terms'))
    pay_in = models.CharField(
        max_length=50, choices=pay_choices, default='once')
    pay_interval = (('daily', 'daily'), ('weekly', 'weekly'),
                    ('monthly', 'monthly'))
    payment_interval = models.CharField(
        max_length=50, choices=pay_interval, default='daily')
    payment_status = models.ManyToManyField(Payment_status)
    objects = PaymentManager()

    @staticmethod
    def paymentDates_end(customer_id):
        customer = Customers.objects.get(id=customer_id)
        # payment end date of payment and dates of payments
        self = Payment.objects.get(id=customer.payment_id)
        # -1 because the 1st payment happen on the order day
        times = customer.times-1
        order_date = datetime.now().date()
        payment_dates = []

        if self.pay_in.lower() == 'once':
            return {'paying_dates': [customer.start], 'end': customer.start}
        else:
            if self.payment_interval.lower() == 'daily':
                for count in range(customer.times):
                    payment_dates.append(
                        customer.start + timedelta(days=count))

                end_date = customer.start + timedelta(days=times)

                return {'paying_dates': payment_dates, 'end': end_date}
            elif self.payment_interval.lower() == 'weekly':
                for count in range(customer.times):
                    payment_dates.append(
                        customer.start + timedelta(days=count*7))

                end_date = customer.start + timedelta(days=times*7)

                return {'paying_dates': payment_dates, 'end': end_date}
            else:
                # get number of days in current month(moth order take place)
                days_in_month = monthrange(
                    order_date.year, order_date.month)[1]

                for count in range(customer.times):
                    payment_dates.append(
                        customer.start + timedelta(days=count*days_in_month))

                end_date = customer.start + timedelta(days=times*days_in_month)

                return {'paying_dates': payment_dates, 'end': end_date}

    @staticmethod
    def paying_in_terms(customer_id):
        # amount of money pay by term
        customer = Customers.objects.get(id=customer_id)
        self = Payment.objects.get(id=customer.payment_id)
        if self.pay_in.lower() == 'terms':
            return round(int(Orders.paying(customer.order_id))/int(customer.times))

    @staticmethod
    def completed(customer_id):
        if Payment.paymentDates_end(customer_id)['end'] == datetime.now().date():
            return True
        else:
            return False

    def __str__(self):
        return PaymentMethods.objects.get(id=self.method_id).name

    def create(self, *args, **kwargs):
        if self.pay_in.lower() == 'once':
            self.payment_interval = 'daily'

        return super().save(*args, **kwargs)


class ProductOrdered(models.Model):
    product = models.ForeignKey(
        Tires, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    custome_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @staticmethod
    def product_price(id):
        self = ProductOrdered

        p_o = self.objects.get(id=id)
        if p_o.custome_price == 0:
            product = Tires.objects.get(id=p_o.product_id)
            return product.price*p_o.quantity
        else:
            product = p_o.custome_price
            return product*p_o.quantity

    # def save(self, *args, **kwargs):
    #     # check if quantity > 0
    #     if int(self.quantity) <= 0:
    #         raise Exception("Ordered product(s) quantity must be > 0")
    #     return super().save(*args, **kwargs)


class Orders(models.Model):
    product_ordered = models.ManyToManyField(ProductOrdered)
    order_on = models.DateField(auto_now=True)
    order_at = models.TimeField(auto_now=True)
    warehouse_id = models.IntegerField(default=1)
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
        products = self.product_ordered.all().values()
        for product in products:
            total_price += ProductOrdered.product_price(product['id'])

        return total_price


class Credentials(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(
        max_length=255, default='None', null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    tel_number = models.CharField(
        max_length=50, default='None', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.email != None:
            credential = Credentials.objects.filter(email=self.email)
            if credential.count() > 0:
                # get the existing credential obj
                return Credentials.objects.get(id=credential.values()[0]['id'])
        return super().save(*args, **kwargs)


class Customers(models.Model):
    credential = models.ForeignKey(Credentials, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING)
    times = models.IntegerField()
    start = models.DateField()
    objects = CustomerManager()

    @staticmethod
    def total():
        return Customers.objects.all().count()

    def __str__(self):
        return Credentials.objects.get(id=self.credential_id).name


@receiver(post_save, sender=Customers)
def track_payment_status(sender, instance, created, **kwargs):
    if created:
        customer_id = instance.id
        payment_dates = Payment.paymentDates_end(customer_id)['paying_dates']

        for pd in payment_dates:
            # create payment status
            p_status = Payment_status.objects.create(payment_date=pd)
            # get created payment object
            payment = Payment.objects.get(id=instance.payment_id)
            # add payment status to payment
            payment.payment_status.add(p_status)
