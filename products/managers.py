from django.db import models
from django.db.models import Q
# from .models import Tires
from datetime import datetime
import json


def get_related(obj, parent, obj_id):
    """
    get related model data of a foreign key relation

    Args:
        obj ([model class]): [related model class]
        parent ([model class]): [model class with the foreign key]
        obj_id ([int]): [related model object id]

    Returns:
        [array]: [array with related object data]
    """
    related_arr = []
    for p in parent.values():
        related = obj.objects.filter(id=p[obj_id]).values()
        for r in related:
            related_arr.append(r)

    return related_arr


class ProductManager(models.Manager):
    # tires = None

    # def __init__(self, tires_model):
    #     self.tires = tires_model

    def get_incoming_products(self, dte=None):
        from .models import Tires
        """
        get incomming product base on the give date

        Args:
            dte ([date], optional): [current date if none else give date]. Defaults to None.

        Returns:
            [obj]: [products data]
        """
        current_date = datetime.now()

        if dte == None:
            # get products of the current date
            added_products = self.select_related().filter(
                add_on=current_date.date())

            return {
                'products': added_products.values(),
                # 'tire': [get_related(Tires, id=product['tire_id']) for product in added_products],
                'tire': get_related(Tires, added_products, 'tire_id'),
                'count': added_products.count()
            }
        else:
            # get products base on give date
            added_products = self.select_related().filter(
                add_on=dte)

            return {
                'products': added_products.values(),
                'tire': get_related(Tires, added_products, 'tire_id'),
                'count': added_products.count()
            }

    def all_products(self):
        from .models import Tires
        products = None

        product_obj = self.select_related().all()

        products = {
            'products': product_obj.values(),
            'tire': get_related(Tires, product_obj, 'tire_id'),
            'count': product_obj.count()
        }

        return products

    def filter_products(self, vehicle, brands, profiles):
        from .models import Tires, Vehicule, Brands, Profiles
        try:
            vehicle = Vehicule.objects.get(name=vehicle).id
        except:
            vehicle = 0

        tires = Tires.objects.filter(
            Q(brands__in=[Brands.objects.get(name=brand)
                          for brand in brands['brands']]) &
            Q(profiles__in=[Profiles.objects.get(name=profile)
                            for profile in profiles['profiles']]) &
            Q(vehicule_id=vehicle)
        )

        return {'tire': tires.values()}


class BrandsManager(models.Manager):
    def all_brands(self):
        brands = self.get_queryset().all()

        return brands


class ProfilesManager(models.Manager):
    def all_profiles(self):
        profiles = self.get_queryset().all()

        return profiles
