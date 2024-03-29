# from products.models import Transfers
from django.db import models
from django.db.models import Q, Sum, Count
from django.core.exceptions import NON_FIELD_ERRORS, ObjectDoesNotExist
from django.contrib.auth.models import User
# from .models import Tires
from datetime import datetime
import json
from django.db.models import Sum
import uuid


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

        brands_arr = ','.join(sorted(kwargs['brands'])) if len(
            kwargs['brands']) > 0 else None
        # kwargs['brands']) > 0 else "{}".format(sorted(kwargs['brands'][0]))
        profile_arr = ','.join(sorted(kwargs['profiles'])) if len(
            kwargs['profiles']) > 0 else None
        # kwargs['profiles']) > 0 else '{}'.format(sorted(kwargs['profiles'][0]))

        if kwargs['vehicle'] != None:
            try:
                global vehicle
                vehicle = Vehicule.objects.get(name=vehicle_name)
            except ObjectDoesNotExist:
                global vehucle
                vehicle = Vehicule.objects.create(name=vehicle_name)
            
            this_tire = Tires.objects.filter(
                Q(size=kwargs['size']) &
                Q(profiles_str=profile_arr) &
                Q(brands_str=brands_arr) &
                Q(vehicule=vehicle)
            )
        else:
            this_tire = Tires.objects.filter(
                Q(size=kwargs['size']) &
                Q(profiles_str=profile_arr) &
                Q(brands_str=brands_arr) 
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
                    warehouse_id=kwargs['user_id'],
                    tire_uid=uuid.uuid4()
                )
                tire.save()
            else:
                tire = Tires.objects.create(
                    size=kwargs['size'],
                    price=kwargs['price'],
                    quantity=kwargs['quantity'],
                    profiles_str=profile_arr,
                    brands_str=brands_arr,
                    warehouse_id=kwargs['user_id'],
                    tire_uid=uuid.uuid4()
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

            return {'created': True, 'msg': 'Product added','product_id': product.id}
        else:
            # updated_qty = int(this_tire.values()[
            #     0]['quantity']) + int(kwargs['quantity'])
            # # update quantity
            # this_tire.update(quantity=updated_qty)

            return {'created': False, 'msg': 'Product already exists', 'product_id': None}  #Products.objects.get(tire_id=this_tire.values()[0]['id']).id

    def update_product(self, **kwargs):
        from products.models import Products, Tires, Brands, Profiles, Vehicule

        brands_arr = ','.join(sorted(kwargs['brands'])) if len(
            kwargs['brands']) > 0 else None
        # kwargs['brands']) > 0 else "{}".format(sorted(kwargs['brands'][0]))
        profile_arr = ','.join(sorted(kwargs['profiles'])) if len(
            kwargs['profiles']) > 0 else None
        # kwargs['profiles']) > 0 else '{}'.format(sorted(kwargs['profiles'][0]))

        try:
            tires = Tires.objects.filter(tire_uid=kwargs['tire_uid'])
            current_tire = Tires.objects.filter(id=kwargs['tire_id'])
        except Exception as e:
            return {'updated': False, 'msg': 'Something went wrong, refresh the page and try it again'}
        
        if kwargs['vehicle'] != None:
            vehicle = Vehicule.objects.get(name=kwargs['vehicle'])
            tires.update(
                size=kwargs['size'],
                price=kwargs['price'],
                vehicule=vehicle,
                profiles_str=profile_arr,
                brands_str=brands_arr
            )
        else:
            tires.update(
                size=kwargs['size'],
                price=kwargs['price'],
                profiles_str=profile_arr,
                brands_str=brands_arr
            )
            
        #update tire qty
        if int(kwargs['quantity']) > 0:
            # current_qty = current_tire.values()[0]['quantity']
            # new_qty = int(current_qty) + int(kwargs['quantity'])
            # update qty
            current_tire.update(updated_pending_qty=kwargs['quantity'])
            # change product status to pending
            Products.objects.filter(tire_id=current_tire.values()[0]['id']).update(status='pending')
            
        # update date and time
        Products.objects.filter(tire=Tires.objects.get(id=current_tire.values()[0]['id'])).update(
            add_on=datetime.now().date(),
            add_at=datetime.now().time()
        )
                
        
        for i in range(tires.count()):

            # update brands
            tires[i].brands.all().delete()
            for brand in kwargs['brands']:
                try:
                    b = Brands.objects.get(name=brand)
                except ObjectDoesNotExist:
                    b = Brands.objects.create(name=brand)

                tires[i].brands.add(b)

            # update profiles
            tires[i].profiles.all().delete()
            for profile in kwargs['profiles']:
                try:
                    p = Profiles.objects.get(name=profile)
                except ObjectDoesNotExist:
                    p = Profiles.objects.create(name=profile)

                tires[i].profiles.add(p)

        return {'updated': True, 'product_id': Products.objects.get(tire_id=tires.values()[0]['id']).id}

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
        product_obj = Tires.objects.filter(products__status='accepted').values(
            ) if user_id == 0 else Tires.objects.filter(Q(warehouse_id=user_id) & Q(products__status='accepted')).values()

        for product in product_obj:
            qty += product['quantity']
            try:
                vehicle = Tires.objects.get(
                    id=product['tire_id']).vehicule.name
            except:
                vehicle = None
            try:
                productsArr.append(
                    {
                        # 'add_at': product['add_at'],
                        # 'add_on': product['add_on'],
                        # 'id': product['id'],
                        'tire': product,
                        'warehouse':  User.objects.get(id=product['warehouse_id']).username,
                        'id': self.get_queryset().get(tire_id=product['id']).id,
                        'brands': Tires.objects.get(id=product['id']).brands.all().values(),
                        'profiles': Tires.objects.get(id=product['id']).profiles.all().values(),
                        'vehicle': vehicle
                    }
                )
                # products = Tires.objects.values('size').annotate(Sum('quantity'))
            except Exception as e:
                print('delete tire', e)
                pass

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
        from orders.models import ProductOrdered

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

        
        if vehicle != 'noname':
            results = Tires.objects.filter(
                Q(brands_str=brand) &
                Q(profiles_str=profile) &
                Q(vehicule_id=vehicle_id) &
                Q(warehouse_id=warehouse_id) &
                Q(products__status='accepted')
            )
        elif vehicle == 'noname' and len(brands['brands']) > 0 and len(profiles['profiles']) > 0:
            tires = Tires.objects.filter(
                Q(brands_str=brand) &
                Q(profiles_str=profile) &
                Q(warehouse_id=warehouse_id) &
                Q(products__status='accepted')
            )
            results = tires if tires.count() > 0 else Tires.objects.filter(warehouse_id=warehouse_id)
        elif len(brands['brands']) == 0 and len(profiles['profiles']) == 0 and vehicle == 'noname':
            results = Tires.objects.filter(Q(warehouse_id=warehouse_id) & Q(products__status='accepted'))
        else:
            results = Tires.objects.filter(
                Q(brands_str=brand) &
                Q(profiles_str=profile) &
                Q(warehouse_id=warehouse_id) &
                Q(products__status='accepted')
            )
            
        results_arr = []
        for result in results.values():
            results_arr.append(
                {
                    # 'sale_qty': p_o.aggregate(Sum('quantity'))['quantity__sum'] if p_o.count() > 0 else 0,
                    'sale_qty': ProductOrdered().get_pending_qty(result['id']),
                    'brands_str': result['brands_str'],
                    'id': result['id'],
                    'pending_qty': result['pending_qty'],
                    'price': result['price'],
                    'profiles_str': result['profiles_str'],
                    'quantity': result['quantity'],
                    'size': result['size'],
                    'vehicule_id': result['vehicule_id'],
                    'warehouse_id': result['warehouse_id'],
                }
            )

        return {'tire': results_arr, 'v': vehicle_id}
    
    def transfer_product_waiting(self, **kwargs):
        from .models import Transfers
        from orders.models import ProductOrdered
        
        brands_arr = ','.join(sorted(kwargs['brands'])) if len(
            kwargs['brands']) > 0 else None
        
        profile_arr = ','.join(sorted(kwargs['profiles'])) if len(
            kwargs['profiles']) > 0 else None
        
        vehicle = kwargs['vehicle'] if kwargs['vehicle'] != None else None
        
        # in case the product is pending in other warehouse(s) check if the transfer qty <= currentQty - pending QTy
        # get product current qty
        product_qty = kwargs['current_qty']
        #pending qty
        pending_qty = 0
        # get pending qty
        pendings = Transfers.objects.filter(
            Q(size=kwargs['size']) &
            Q(brands=brands_arr) &
            Q(profiles=profile_arr) &
            Q(vehicle=vehicle) &
            Q(price=kwargs['price']),
            Q(status='pending')
        )
        
        for p_qty in pendings.values():
            pending_qty += p_qty['quantity']
            
        # not validated sales
        pending_sales_qty = ProductOrdered().get_pending_qty(kwargs['tire_id'])
        print('pending sales', pending_sales_qty)
            
        qty_remain = int(product_qty) - (int(pending_qty) + int(pending_sales_qty))
        
        if int(qty_remain) < int(kwargs['qty']):
            return {'transfered': False, 'msg': 'This product is pending in one or more warehouse(s) and/or pending in sales. The remain quantity({}) is lesser than the quantity you want to transfer'.format(qty_remain), 'status': 'Pending'}
        else:
            transfer = Transfers.objects.create(
                sender=kwargs['sender_id'],
                sender_name=User.objects.get(id=kwargs['sender_id']).username,
                receiver=kwargs['receiver_name'],
                size=kwargs['size'],
                price=kwargs['price'],
                vehicle=vehicle,
                profiles=profile_arr,
                brands=brands_arr,
                quantity=kwargs['qty'],
                tire_uid=kwargs['tire_uid']
            )
            transfer.save()
            
            return {'transfered': True, 'msg': 'Product transfered', 'status': 'Pending'}

    def transfer_product(self, **kwargs):
        from .models import Tires, Vehicule, Brands, Profiles, Products, Transfers
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
        
        product_by_sender = Tires.objects.filter(
                Q(tire_uid=kwargs['tire_uid']),
                Q(warehouse_id=sender_id)
            )

        
        product_by_receiver = Tires.objects.filter(
                Q(tire_uid=kwargs['tire_uid']),
                Q(warehouse_id=receiver_wh_id.id)
            )
        
        
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
                    warehouse_id=receiver_wh_id.id,
                    tire_uid=kwargs['tire_uid']
                )
                tire.save()
            else:
                tire = Tires.objects.create(
                    size=kwargs['size'],
                    price=kwargs['price'],
                    quantity=kwargs['qty'],
                    profiles_str=profile_arr,
                    brands_str=brands_arr,
                    warehouse_id=receiver_wh_id.id,
                    tire_uid=kwargs['tire_uid']
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
            Products.objects.create(tire=tire, status='accepted')
        else:
            # update receiver product qty
            current_receiver_qty = product_by_receiver.values()[0]['quantity']
            new_qty = int(current_receiver_qty) + int(kwargs['qty'])
            product_by_receiver.update(quantity=new_qty)
            
        # update pending qty
        Tires.objects.filter(
            Q(tire_uid=kwargs['tire_uid']),
            Q(warehouse_id=sender_id)
        ).update(pending_qty=0)

        # update sender product quantity
        try:
            current_qty = product_by_sender.values()[0]['quantity']
            qty_tranfered = kwargs['qty']
            new_qty = int(current_qty) - int(qty_tranfered)
            product_by_sender.update(quantity=new_qty)
        except :
            return {'transfered': False, 'msg': 'Somethink went wrong, try to update this product from the sender warehouse and try again.', 'error': True}

        return {'transfered': True, 'msg': 'Product transfered', 'error': False}
    

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
        
        pending = self.get_queryset().filter(
            Q(send_on=dte) & Q(status='pending')
        ) if wh_id==0 else self.get_queryset().filter(
            Q(send_on=dte) &
            Q(status='pending') &
            Q(sender=wh_id)
        )
        
        # transfer = {
        #     'sender_name': User.objects.get(id=transfers.values()[0]['sender']).username,
        #     'data': transfers.values()
        # }
            
        return {'transfers': transfers.values(), 'count': pending.count()}
    
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
        
        pending = self.get_queryset().filter(
            Q(send_on=dte) & Q(status='pending')
        ) if wh_id==0 else self.get_queryset().filter(
            Q(send_on=dte) &
            Q(status='pending') &
            Q(receiver=receiver_name)
        )
        
        processed_transfers_count =  self.get_queryset().filter(
            Q(status='accept') | Q(status='reject')
        ).count()
        
        pending_transfers_count =  self.get_queryset().filter(status='pending').count()
            
        return {
            'receives': receives.values(), 
            'count': pending.count(), 
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
