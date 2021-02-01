from django.db import models
from .managers import *
from django.db.models import Q

# Create your models here.


class Brands(models.Model):
    name = models.CharField(max_length=255)
    objects = BrandsManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        brand = Brands.objects.filter(name=self.name)
        if brand.count() > 0:
            # get the existing credential obj
            raise Exception('This brand already exists')
        return super().save(*args, **kwargs)


class Vehicule(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profiles(models.Model):
    name = models.CharField(max_length=255)
    objects = ProfilesManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        profile = Profiles.objects.filter(name=self.name)
        if profile.count() > 0:
            # get the existing credential obj
            raise Exception('This profile already exists')
        return super().save(*args, **kwargs)


class Tires(models.Model):
    size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brands = models.ManyToManyField(Brands)
    profiles = models.ManyToManyField(Profiles)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    profiles_str = models.CharField(max_length=255)
    brands_str = models.CharField(max_length=255)

    def __str__(self):
        return self.size

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
