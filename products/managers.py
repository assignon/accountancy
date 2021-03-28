from django.db import models
from django.db.models import Q, Sum, Count
from django.core.exceptions import NON_FIELD_ERRORS, ObjectDoesNotExist
from django.contrib.auth.models import User
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

        vehicle_name = kwargs['vehicle']
        try:
            global vehicle
            if kwargs['vehicle'] != None:
                vehicle = Vehicule.objects.get(name=vehicle_name)
        except ObjectDoesNotExist:
            global vehucle
            if kwargs['vehicle'] != None:
                vehicle = Vehicule.objects.create(name=vehicle_name)

        brands_arr = ','.join(sorted(kwargs['brands'])) if len(
            kwargs['brands']) > 0 else None
        # kwargs['brands']) > 0 else "{}".format(sorted(kwargs['brands'][0]))
        profile_arr = ','.join(sorted(kwargs['profiles'])) if len(
            kwargs['profiles']) > 0 else None
        # kwargs['profiles']) > 0 else '{}'.format(sorted(kwargs['profiles'][0]))

        this_tire = Tires.objects.filter(
            Q(size=kwargs['size']) &
            Q(profiles_str=profile_arr) &
            Q(brands_str=brands_arr) &
            Q(price=kwargs['price'])
        )

        if this_tire.count() == 0:
            # add tire
            # add vehicle if is not none
            if kwargs['vehicle'] != None:
                tire = Tires.objects.create(
                    size=kwargs['size'],
                    price=kwargs['price'],
                    quantity=kwargs['quantity'],
                    vehicule=vehicle,
                    profiles_str=profile_arr,
                    brands_str=brands_arr,
                    warehouse_id=kwargs['user_id']
                )
                tire.save()
            else:
                tire = Tires.objects.create(
                    size=kwargs['size'],
                    price=kwargs['price'],
                    quantity=kwargs['quantity'],
                    profiles_str=profile_arr,
                    brands_str=brands_arr,
                    warehouse_id=kwargs['user_id']
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

        brands_arr = ','.join(sorted(kwargs['brands'])) if len(
            kwargs['brands']) > 0 else None
        # kwargs['brands']) > 0 else "{}".format(sorted(kwargs['brands'][0]))
        profile_arr = ','.join(sorted(kwargs['profiles'])) if len(
            kwargs['profiles']) > 0 else None
        # kwargs['profiles']) > 0 else '{}'.format(sorted(kwargs['profiles'][0]))

        try:
            tire = Tires.objects.filter(id=kwargs['tire_id'])
            tire_obj = Tires.objects.get(id=kwargs['tire_id'])
        except:
            return {'updated': False, 'msg': 'Something went wrong, refresh the page and try it again'}

        if kwargs['vehicle'] != None:
            vehicle = Vehicule.objects.get(name=kwargs['vehicle'])
            tire.update(
                size=kwargs['size'],
                price=kwargs['price'],
                quantity=kwargs['quantity'],
                vehicule=vehicle,
                profiles_str=profile_arr,
                brands_str=brands_arr
            )
        else:
            tire.update(
                size=kwargs['size'],
                price=kwargs['price'],
                quantity=kwargs['quantity'],
                profiles_str=profile_arr,
                brands_str=brands_arr
            )
            
        # update date and time
        Products.objects.filter(tire=tire_obj).update(
            add_on=datetime.now().date(),
            add_at=datetime.now().time()
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

    def all_products(self, user_id):
        from .models import Tires
        products = None
        productsArr = []
        qty = 0  # tire quantity

        # product_obj = self.select_related().all()
        try:
            product_obj = Tires.objects.all().values(
            ) if user_id == 0 else Tires.objects.filter(warehouse_id=user_id).values()
        except:
            pass

        for product in product_obj:
            qty += product['quantity']
            try:
                vehicle = Tires.objects.get(
                    id=product['tire_id']).vehicule.name
            except:
                vehicle = None
            productsArr.append(
                {
                    # 'add_at': product['add_at'],
                    # 'add_on': product['add_on'],
                    # 'id': product['id'],
                    'tire': product,
                    'id': self.get_queryset().get(tire_id=product['id']).id,
                    'brands': Tires.objects.get(id=product['id']).brands.all().values(),
                    'profiles': Tires.objects.get(id=product['id']).profiles.all().values(),
                    'vehicle': vehicle
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
            try:
                vehicle = Tires.objects.get(
                    id=product['tire_id']).vehicule.name
            except:
                vehicle = None
            productsArr.append(
                {
                    'add_at': product['add_at'],
                    'add_on': product['add_on'],
                    'id': product['id'],
                    'tire': get_related(Tires, product_obj, 'tire_id'),
                    'brands': Tires.objects.get(id=product['tire_id']).brands.all().values(),
                    'profiles': Tires.objects.get(id=product['tire_id']).profiles.all().values(),
                    'vehicle': vehicle,
                    'warehouse': User.objects.get(id=get_related(Tires, product_obj, 'tire_id')[0]['warehouse_id']).username
                }
            )

        return {'products': productsArr}

    def filter_products(self, vehicle, brands, profiles, warehouse_id):
        from .models import Tires, Vehicule

        vehicle_id = Vehicule.objects.get(
            name=vehicle).id if vehicle != 'noname' else None

        try:
            vehicle_id = Vehicule.objects.get(
                name=vehicle).id
        except:
            vehicle_id = None

        # tires = Tires.objects.filter(
        #     Q(brands__in=[Brands.objects.get(name=brand)
        #                   for brand in brands['brands']]) &
        #     Q(profiles__in=[Profiles.objects.get(name=profile)
        #                     for profile in profiles['profiles']]) &
        #     Q(vehicule_id=vehicle)
        # )

        brand = ','.join(sorted(brands['brands'])) if len(
            brands['brands']) > 0 else None
        profile = ','.join(sorted(profiles['profiles'])) if len(
            profiles['profiles']) > 0 else None

        if len(brands['brands']) > 0 and len(profiles['profiles']) > 0 and vehicle != 'noname':
            results = Tires.objects.filter(
                Q(brands_str=brand) &
                Q(profiles_str=profile) &
                Q(vehicule_id=vehicle_id) &
                Q(warehouse_id=warehouse_id)
            )
        elif len(brands['brands']) == 0 and len(profiles['profiles']) == 0 and vehicle != 'noname':
            results = Tires.objects.filter(
                Q(vehicule_id=vehicle_id) &
                Q(warehouse_id=warehouse_id)
            )
        elif len(brands['brands']) == 0 and len(profiles['profiles']) == 0:
            tires = Tires.objects.filter(
                Q(brands_str=None) &
                Q(profiles_str=None) &
                Q(warehouse_id=warehouse_id)
            )
            results = tires if tires.count() > 0 else Tires.objects.all()
        else:
            results = Tires.objects.filter(
                Q(brands_str=brand) &
                Q(profiles_str=profile) &
                Q(warehouse_id=warehouse_id)
            )

        # if len(brands['brands']) > 0 and len(profiles['profiles']) > 0 and vehicle != None:
        #     results = Tires.objects.filter(
        #         Q(brands_str=','.join(sorted(brands['brands']))) &
        #         Q(profiles_str=','.join(sorted(profiles['profiles']))) &
        #         Q(vehicule_id=vehicle) &
        #         Q(warehouse_id=warehouse_id)
        #     )
        # elif len(brands['brands']) == 0 and len(profiles['profiles']) > 0 and vehicle != None:
        #     results = Tires.objects.filter(
        #         Q(profiles_str=','.join(sorted(profiles['profiles']))) &
        #         Q(vehicule_id=vehicle) &
        #         Q(warehouse_id=warehouse_id)
        #     )
        # elif len(brands['brands']) > 0 and len(profiles['profiles']) == 0 and vehicle != None:
        #     results = Tires.objects.filter(
        #         Q(brands_str=','.join(sorted(brands['brands']))) &
        #         Q(vehicule_id=vehicle) &
        #         Q(warehouse_id=warehouse_id)
        #     )
        # elif len(brands['brands']) > 0 and len(profiles['profiles']) > 0 and vehicle == None:
        #     results = Tires.objects.filter(
        #         Q(brands_str=','.join(sorted(brands['brands']))) &
        #         Q(profiles_str=','.join(sorted(profiles['profiles']))) &
        #         Q(warehouse_id=warehouse_id)
        #     )
        # elif len(brands['brands']) == 0 and len(profiles['profiles']) == 0 and vehicle != None:
        #     results = Tires.objects.filter(
        #         Q(vehicule_id=vehicle) &
        #         Q(warehouse_id=warehouse_id)
        #     )
        # else:
        #     tires = Tires.objects.filter(
        #         Q(brands_str=None) &
        #         Q(profiles_str=None) &
        #         Q(warehouse_id=warehouse_id)
        #     )
        #     results = tires if tires.count() > 0 else Tires.objects.all()

        return {'tire': results.values(), 'v': vehicle_id}
    
    def transfer_product_waiting(self, **kwargs):
        from .models import Transfers
        
        brands_arr = ','.join(sorted(kwargs['brands'])) if len(
            kwargs['brands']) > 0 else None
        
        profile_arr = ','.join(sorted(kwargs['profiles'])) if len(
            kwargs['profiles']) > 0 else None
        
        vehicle = kwargs['vehicle'] if kwargs['vehicle'] != None else None

        transfer = Transfers.objects.create(
            sender=kwargs['sender_id'],
            sender_name=User.objects.get(id=kwargs['sender_id']).username,
            receiver=kwargs['receiver_name'],
            size=kwargs['size'],
            price=kwargs['price'],
            vehicle=vehicle,
            profiles=profile_arr,
            brands=brands_arr,
            quantity=kwargs['qty']
        )
        transfer.save()
        
        return {'transfered': True, 'msg': 'Product transfered', 'status': 'Pending'}

    def transfer_product(self, **kwargs):
        from .models import Tires, Vehicule, Brands, Profiles, Products
        from django.contrib.auth.models import User

        receiver_wh_id = User.objects.get(username=kwargs['receiver_name'])
        sender_id = kwargs['sender_id']
        vehicle_name = kwargs['vehicle']
        try:
            global vehicle
            if kwargs['vehicle'] != None:
                vehicle = Vehicule.objects.get(name=vehicle_name)
        except ObjectDoesNotExist:
            global vehucle
            if kwargs['vehicle'] != None:
                vehicle = Vehicule.objects.create(name=vehicle_name)
        # if len(kwargs['brands']) > 0 and len(kwargs['profiles']) > 0
        print('bbbrrrnnddd', kwargs['brands'])
        print('prrooofffiiillee', kwargs['profiles'])
        if kwargs['vehicle'] != None:
            product_by_sender = Tires.objects.filter(
                Q(size=kwargs['size']) &
                Q(brands_str=','.join(sorted(kwargs['brands'])) if len(
                    kwargs['brands']) > 0 else None) &
                Q(profiles_str=','.join(sorted(kwargs['profiles'])) if len(
                    kwargs['profiles']) > 0 else None) &
                Q(vehicule=vehicle) &
                Q(warehouse_id=sender_id)
            )
        else:
            product_by_sender = Tires.objects.filter(
                Q(size=kwargs['size']) &
                Q(brands_str=','.join(sorted(kwargs['brands'])) if len(
                    kwargs['brands']) > 0 else None) &
                Q(profiles_str=','.join(sorted(kwargs['profiles'])) if len(
                    kwargs['profiles']) > 0 else None) &
                Q(warehouse_id=sender_id)
            )

        brands_sorted = ','.join(sorted(kwargs['brands'])) if len(
                    kwargs['brands']) > 0 else None
        profiles_sorted = ','.join(sorted(kwargs['profiles'])) if len(
                    kwargs['profiles']) > 0 else None
        
        if kwargs['vehicle'] != None:
            product_by_receiver = Tires.objects.filter(
                Q(size=kwargs['size']) &
                Q(brands_str=brands_sorted) &
                Q(profiles_str=profiles_sorted) &
                Q(vehicule=vehicle) &
                Q(warehouse_id=receiver_wh_id.id)
            )
        else:
            product_by_receiver = Tires.objects.filter(
                Q(size=kwargs['size']) &
                Q(brands_str=brands_sorted) &
                Q(profiles_str=profiles_sorted) &
                Q(warehouse_id=receiver_wh_id.id)
            )
        print('receiver counntt', product_by_receiver.count())
        if product_by_receiver.count() == 0:
            # create
            brands_arr = ','.join(sorted(kwargs['brands'])) if len(
                kwargs['brands']) > 0 else None
            profile_arr = ','.join(sorted(kwargs['profiles'])) if len(
                kwargs['profiles']) > 0 else None

            # add tire
            if kwargs['vehicle'] != None:
                tire = Tires.objects.create(
                    size=kwargs['size'],
                    price=kwargs['price'],
                    quantity=kwargs['qty'],
                    vehicule=vehicle,
                    profiles_str=profile_arr,
                    brands_str=brands_arr,
                    warehouse_id=receiver_wh_id.id
                )
                tire.save()
            else:
                tire = Tires.objects.create(
                    size=kwargs['size'],
                    price=kwargs['price'],
                    quantity=kwargs['qty'],
                    profiles_str=profile_arr,
                    brands_str=brands_arr,
                    warehouse_id=receiver_wh_id.id
                )
                tire.save()

            # add brands to tire
            if len(kwargs['brands']) > 0:
                for brand in kwargs['brands']:
                    tire.brands.add(Brands.objects.get(name=brand))
            # add profiles to tire
            if len(kwargs['profiles']) > 0:
                for profile in kwargs['profiles']:
                    tire.profiles.add(Profiles.objects.get(name=profile))
            # add tire to product
            Products.objects.create(tire=tire)
        else:
            # update receiver product qty
            current_receiver_qty = product_by_receiver.values()[0]['quantity']
            new_qty = int(current_receiver_qty) + int(kwargs['qty'])
            product_by_receiver.update(quantity=new_qty)

        # update sender product quantity
        current_qty = product_by_sender.values()[0]['quantity']
        qty_tranfered = kwargs['qty']
        new_qty = int(current_qty) - int(qty_tranfered)
        product_by_sender.update(quantity=new_qty)

        return {'transfered': True, 'msg': 'Product transfered'}
    

class TransferManager(models.Manager):
    def transfers(self, sender_id, dte, wh_id):
        """
        get sended products filter by date and sender/warehouse/user id

        Args:
            sender_id (int): [warehouse/sender/user id]
            dte (date): [date]
            wh_id (int): [id of warehouse, if 0 => admin connect and can see everything]
        """
        transfers = self.get_queryset().filter(
            send_on=dte
        ) if wh_id==0 else self.get_queryset().filter(
            Q(send_on=dte) &
            Q(sender=wh_id)
        )
        
        # transfer = {
        #     'sender_name': User.objects.get(id=transfers.values()[0]['sender']).username,
        #     'data': transfers.values()
        # }
            
        return {'transfers': transfers.values(), 'count': transfers.count()}
    
    def receives(self, receiver_name, dte, wh_id):
        """
        get received products filter by date and sender/warehouse/user name

        Args:
            receiver_name (str): [name of the warehouse/username]
            dte (date): [date]
            wh_id (int): [id of warehouse, if 0 => admin connect and can see everything]
        """
        receives = self.get_queryset().filter(
            send_on=dte
        ) if wh_id==0 else self.get_queryset().filter(
            Q(send_on=dte) &
            Q(receiver=receiver_name)
        )
        
        processed_transfers_count =  self.get_queryset().filter(
            Q(status='accept') | Q(status='reject')
        ).count()
        
        pending_transfers_count =  self.get_queryset().filter(status='pending').count()
            
        return {
            'receives': receives.values(), 
            'count': receives.count(), 
            'processed_transfers': processed_transfers_count, 
            'pending_transfers': pending_transfers_count
        }
    
    def transfer_details(self, transfer_id):
        """
        get a transfer/receive product details

        Args:
            id (int): [id of sender/user/warehouse]
        """
        details = self.get_queryset().filter(id=transfer_id)
        
        return details.values()
    
    def update_transfer_status(self, transfer_id, status):
        """
        set sended product status to accept or reject

        Args:
            status (str): [accept or reject]
        """
        pass

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
