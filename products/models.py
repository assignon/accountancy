from django.db import models
from .managers import ProductManager

# Create your models here.


class Brands(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Vehicule(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profiles(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tires(models.Model):
    size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brands = models.ManyToManyField(Brands)
    profiles = models.ManyToManyField(Profiles)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.DO_NOTHING)

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
