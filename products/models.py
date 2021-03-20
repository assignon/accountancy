from django.db import models
from .managers import *
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.


class Brands(models.Model):
    name = models.CharField(max_length=255)
    objects = BrandsManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        brand = Brands.objects.filter(name=self.name)
        if brand.count() > 0:
            raise Exception('This brand already exists')
        return super().save(*args, **kwargs)


class Vehicule(models.Model):
    name = models.CharField(max_length=100)
    objects = VehicleManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        vehicle = Vehicule.objects.filter(name=self.name)
        if vehicle.count() > 0:
            raise Exception('This brand already exists')
        return super().save(*args, **kwargs)


class Profiles(models.Model):
    name = models.CharField(max_length=255)
    objects = ProfilesManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        profile = Profiles.objects.filter(name=self.name)
        if profile.count() > 0:
            raise Exception('This profile already exists')
        return super().save(*args, **kwargs)
    
class Transfers(models.Model):
    sender = models.IntegerField()
    sender_name = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle = models.CharField(max_length=255, null=True, blank=True)
    profiles = models.CharField(max_length=255, null=True, blank=True)
    brands = models.CharField(max_length=255, null=True, blank=True)
    quantity =  models.IntegerField(default=1)
    status = models.CharField(max_length=100, default='pending') # pending, accepted, refused
    send_on = models.DateField(auto_now=True)
    objects = TransferManager()
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return str(self.sender)

class Tires(models.Model):
    size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brands = models.ManyToManyField(Brands)
    profiles = models.ManyToManyField(Profiles)
    vehicule = models.ForeignKey(
        Vehicule, on_delete=models.DO_NOTHING, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    profiles_str = models.CharField(max_length=255, null=True, blank=True)
    brands_str = models.CharField(max_length=255, null=True, blank=True)
    warehouse_id = models.IntegerField(default=1)  # user id

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.size

    @staticmethod
    def is_su(user_id):
        user = User.objects.get(id=user_id)

        return True if user.is_superuser else False

    # def save(self, *args, **kwargs):
    #     this_tire = Tires.objects.filter(size=self.size)

    #     if this_tire.count() > 0:
    #         vehicle = Vehicule.objects.get(id=self.vehicule_id)
    #         brands = Brands.objects.filter(
    #             tires__id=this_tire.values()[0]['id']).count()
    #         profiles = Profiles.objects.filter(
    #             tires__id=this_tire.values()[0]['id']).count()
    #         tire_vehicle = Tires.objects.filter(vehicule_id=vehicle.id).count()

    #         if brands > 0 and profiles > 0 and tire_vehicle > 0:
    #             updated_qty = int(this_tire.values()[
    #                               0]['quantity']) + int(self.quantity)
    #             # update quantity
    #             this_tire.update(quantity=updated_qty)
    #             print('tire exist, qty updated', this_tire.values()[
    #                 0]['quantity'])

    #             raise Exception('tire exist')

    #     return super().save(*args, **kwargs)


# info in Products model is important for the admin not raly for the customer
class Products(models.Model):
    tire = models.ForeignKey(Tires, on_delete=models.DO_NOTHING)
    add_on = models.DateField(auto_now=True)
    add_at = models.TimeField(auto_now=True)
    objects = ProductManager()

    @staticmethod
    def total():
        return Products.objects.all().count()

    def __str__(self):
        return Tires.objects.get(id=self.tire_id).size
