from django.db import models
from .managers import *

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

    def __str__(self):
        return self.size


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
