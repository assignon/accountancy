from django.db import models
from django.db.models import Q, Sum, Count
from django.core.exceptions import ObjectDoesNotExist
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

    def add_product(self, **kwargs):
        from products.models import Products, Tires, Brands, Profiles, Vehicule

        try:
            global vehicle
            vehicle = Vehicule.objects.get(name=kwargs['vehicle'])
        except ObjectDoesNotExist:
            global vehucle
            vehicle = Vehicule.objects.create(name=kwargs['vehicle'])

        brands_arr = ','.join(sorted(kwargs['brands'])) if len(
            kwargs['brands']) > 0 else "{}".format(sorted(kwargs['brands'][0]))
        profile_arr = ','.join(sorted(kwargs['profiles'])) if len(
            kwargs['profiles']) > 0 else '{}'.format(sorted(kwargs['profiles'][0]))

        this_tire = Tires.objects.filter(
            Q(size=kwargs['size']) &
            Q(profiles_str=profile_arr) &
            Q(brands_str=brands_arr) &
            Q(price=kwargs['price'])
        )

        if this_tire.count() == 0:
            # add tire
            tire = Tires.objects.create(
                size=kwargs['size'],
                price=kwargs['price'],
                quantity=kwargs['quantity'],
                vehicule=vehicle,
                profiles_str=profile_arr,
                brands_str=brands_arr
            )
            tire.save()
            # get brands
            for brand in kwargs['brands']:
                tire.brands.add(Brands.objects.get(name=brand))
            # get profiles
            for profile in kwargs['profiles']:
                tire.profiles.add(Profiles.objects.get(name=profile))
            # add tire to product
            product = Products.objects.create(tire=tire)

            return {'created': True, 'product_id': product.id}
        else:
            updated_qty = int(this_tire.values()[
                0]['quantity']) + int(kwargs['quantity'])
            # update quantity
            this_tire.update(quantity=updated_qty)

            return {'created': True, 'product_id': Products.objects.get(tire_id=this_tire.values()[0]['id']).id}

    def update_product(self, **kwargs):
        from products.models import Products, Tires, Brands, Profiles, Vehicule

        vehicle = Vehicule.objects.get(name=kwargs['vehicle'])
        brands_arr = ','.join(sorted(kwargs['brands'])) if len(
            kwargs['brands']) > 0 else "{}".format(sorted(kwargs['brands'][0]))
        profile_arr = ','.join(sorted(kwargs['profiles'])) if len(
            kwargs['profiles']) > 0 else '{}'.format(sorted(kwargs['profiles'][0]))

        tire = Tires.objects.filter(id=kwargs['tire_id'])
        tire.update(
            size=kwargs['size'],
            price=kwargs['price'],
            quantity=kwargs['quantity'],
            vehicule=vehicle,
            profiles_str=profile_arr,
            brands_str=brands_arr
        )

        # update brands
        tire[0].brands.all().delete()
        for brand in kwargs['brands']:
            try:
                b = Brands.objects.get(name=brand)
            except ObjectDoesNotExist:
                b = Brands.objects.create(name=brand)

            tire[0].brands.add(b)

        # update profiles
        tire[0].profiles.all().delete()
        for profile in kwargs['profiles']:
            try:
                p = Profiles.objects.get(name=profile)
            except ObjectDoesNotExist:
                p = Profiles.objects.create(name=profile)

            tire[0].profiles.add(p)

        return {'updated': True, 'product_id': Products.objects.get(tire_id=tire.values()[0]['id']).id}

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
        productsArr = []
        qty = 0  # tire quantity

        product_obj = self.select_related().all()

        for product in Tires.objects.all().values():
            qty += product['quantity']
            productsArr.append(
                {
                    # 'add_at': product['add_at'],
                    # 'add_on': product['add_on'],
                    # 'id': product['id'],
                    'tire': product,
                    'id': self.get_queryset().get(tire_id=product['id']).id,
                    'brands': Tires.objects.get(id=product['id']).brands.all().values(),
                    'profiles': Tires.objects.get(id=product['id']).profiles.all().values(),
                    'vehicle': Tires.objects.get(id=product['id']).vehicule.name
                }
            )
            # products = Tires.objects.values('size').annotate(Sum('quantity'))

        products = {
            'products': productsArr,
            'count': qty
        }

        return products

    def product_details(self, product_id):
        from .models import Tires

        productsArr = []
        product_obj = self.select_related().filter(id=product_id)

        for product in product_obj.values():
            productsArr.append(
                {
                    'add_at': product['add_at'],
                    'add_on': product['add_on'],
                    'id': product['id'],
                    'tire': get_related(Tires, product_obj, 'tire_id'),
                    'brands': Tires.objects.get(id=product['tire_id']).brands.all().values(),
                    'profiles': Tires.objects.get(id=product['tire_id']).profiles.all().values(),
                    'vehicle': Tires.objects.get(id=product['tire_id']).vehicule.name
                }
            )

        return {'products': productsArr}

    def filter_products(self, vehicle, brands, profiles):
        from .models import Tires, Vehicule, Brands, Profiles
        try:
            vehicle = Vehicule.objects.get(name=vehicle).id
        except:
            vehicle = 0

        # tires = Tires.objects.filter(
        #     Q(brands__in=[Brands.objects.get(name=brand)
        #                   for brand in brands['brands']]) &
        #     Q(profiles__in=[Profiles.objects.get(name=profile)
        #                     for profile in profiles['profiles']]) &
        #     Q(vehicule_id=vehicle)
        # )

        tires = Tires.objects.filter(
            Q(brands_str=','.join(sorted(brands['brands']))) &
            Q(profiles_str=','.join(sorted(profiles['profiles']))) &
            Q(vehicule_id=vehicle)
        )

        print('brannnddd', ','.join(sorted(brands['brands'])))
        print('prooofffill', ','.join(sorted(profiles['profiles'])))

        return {'tire': tires.values()}


class BrandsManager(models.Manager):
    def all_brands(self):
        brands = self.get_queryset().all()

        return brands


class ProfilesManager(models.Manager):
    def all_profiles(self):
        profiles = self.get_queryset().all()

        return profiles


class VehicleManager(models.Manager):
    def all_vehicles(self):
        vehicles = self.get_queryset().all()

        return vehicles
