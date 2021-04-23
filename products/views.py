# from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model

from django.contrib.auth.models import User
# from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core import serializers
from django.db.models import Q
# from django.http import QueryDict
import json
from datetime import datetime, timedelta
# from django.contrib.auth.hashers import make_password
################################## DRF IMPORTS #######################################
from rest_framework import viewsets
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from products.serializers import ProductSerializer
from .models import Products, Brands, Profiles, Tires, Transfers, Vehicule
from orders.models import ProductOrdered

# Create your views here.


class ProductView(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_product(self, request):
        req = request.data['body']
        data = {
            'size': req['size'],
            'vehicle': req['vehicle'],
            'price': req['price'],
            'quantity': req['quantity'],
            'brands': req['brands']['brands'],
            'profiles': req['profiles']['profiles'],
            'user_id': int(req['user_id'])
        }

        return Response(Products.objects.add_product(**data))

    @csrf_exempt
    @action(methods=['put'], detail=False)
    def update_product(self, request):
        req = request.data['body']
        data = {
            'size': req['size'],
            'vehicle': req['vehicle'],
            'price': req['price'],
            'quantity': req['quantity'],
            'brands': req['brands']['brands'],
            'profiles': req['profiles']['profiles'],
            'tire_id': req['tire_id'],
        }

        return Response(Products.objects.update_product(**data))
    
    @csrf_exempt
    @action(methods=['delete'], detail=False)
    def remove_product(self, request):
        tire_id = request.query_params.get('product_id')
        
        try:
            # check if product is ordered
            product_ordered = ProductOrdered.objects.filter(product_id=tire_id)
            
            if product_ordered.count() == 0:
                product_obj = Products.objects.filter(tire_id=tire_id)
                product_obj.delete()
                # delete tire
                tire_obj = Tires.objects.filter(id=tire_id)
                tire_obj.delete()
                
                return Response({'deleted': True, 'msg': 'Product deleted'})
            else:
                return Response({'deleted': False, 'msg': 'This product has been ordered'})
        except Exception as e:
            return Response({'deleted': False, 'msg': 'Something went wrong {}'.format(e)})
        
        
        

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def products(self, request):
        """
        get all products count from DB

        Args:
            request (dict): [request data]
        """
        user_id = int(request.query_params.get('user_id'))

        products = Products.objects.all_products(user_id)

        return Response(products)

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def filter_products(self, request):
        vehicle = request.query_params.get('vehicle')
        brands = json.loads(request.query_params.get('brands'))
        profiles = json.loads(request.query_params.get('profiles'))
        warehouse_id = request.query_params.get('user_id')

        return Response(Products.objects.filter_products(vehicle, brands, profiles, warehouse_id))

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def product_details(self, request):
        product_id = request.query_params.get('product_id')

        return Response(Products.objects.product_details(product_id))
    
    @csrf_exempt
    @action(methods=['post'], detail=False)
    def transfer_product_waiting(self, request):
        transfer_data = {
            'vehicle': request.data['body']['vehicle'],
            'brands': [brand['name'] for brand in request.data['body']['brands']['brands']],
            'profiles': [profile['name'] for profile in request.data['body']['profiles']['profiles']],
            'qty': request.data['body']['qty'],
            'receiver_name': request.data['body']["receiver_name"],
            'sender_id': request.data['body']['sender_id'],
            'size': request.data['body']['size'],
            'price': request.data['body']['price'],
            'current_qty':  request.data['body']['current_qty']
        }

        return Response(Products.objects.transfer_product_waiting(**transfer_data))

    # @csrf_exempt
    # @action(methods=['post'], detail=False)
    def transfer_product(self, data):
        transfer_data = {
            'vehicle': data['vehicle'],
            # 'brands': [brand['name'] for brand in request.data['body']['brands']['brands']],
            'brands':  data['brands'].split(',') if data['brands']!= None else [],
            # 'profiles': [profile['name'] for profile in request.data['body']['profiles']['profiles']],
            'profiles': data['profiles'].split(',') if data['profiles']!= None else [],
            'qty': data['quantity'],
            'receiver_name': data["receiver"],
            'sender_id': data['sender'],
            'size': data['size'],
            'price': data['price'],
        }

        return Products.objects.transfer_product(**transfer_data)
        # return Response({'data': transfer_data['brands']})
        
    @csrf_exempt
    @action(methods=['get'], detail=False)
    def product_transfered(self, request):
        dte = datetime.now() if request.query_params.get('date')==None else request.query_params.get('date')
        sender_id = request.query_params.get('sender_id')
        wh_id = int(request.query_params.get('wh_id'))
        
        return Response(Transfers.objects.transfers(sender_id, dte, wh_id))
    
    @csrf_exempt
    @action(methods=['get'], detail=False)
    def product_received(self, request):
        dte = datetime.now() if request.query_params.get('date')==None else request.query_params.get('date')
        receiver_name = request.query_params.get('receiver_name')
        wh_id = int(request.query_params.get('wh_id'))
        
        return Response(Transfers.objects.receives(receiver_name, dte, wh_id))
    
    @csrf_exempt
    @action(methods=['get'], detail=False)
    def transfer_details(self, request):
        transfer_id = request.query_params.get('id')
        
        return Response(Transfers.objects.transfer_details(transfer_id))
    
    @csrf_exempt
    @action(methods=['get'], detail=False)
    def update_transfer_status(self, request):
        status = request.query_params.get('status')
        transfer_id = request.query_params.get('transfer_id')
        # update transfer status
        transfer = Transfers.objects.filter(id=transfer_id)
        transfer.update(status=status)
        # update product quantity if transfer accepted
        if status == 'accept':
            transfer = self.transfer_product(transfer.values()[0])
            
            return Response({'updated': True, 'msg': 'Product {}'.format(status), 'error': transfer['error'], 'transfermsg': transfer['msg']})
        else:
            vehicle_name = transfer.values()[0]['vehicle']
            
            if transfer.values()[0]['vehicle'] != None:
                tire = Tires.objects.filter(
                    Q(size=transfer.values()[0]['size']) &
                    Q(brands_str=','.join(sorted(transfer.values()[0]['brands'])) if 
                        transfer.values()[0]['brands'] != None else None) &
                    Q(profiles_str=','.join(sorted(transfer.values()[0]['profiles'])) if 
                        transfer.values()[0]['profiles'] != None else None) &
                    Q(vehicule=Vehicule.objects.get(name=vehicle_name)) &
                    Q(warehouse_id=transfer.values()[0]['sender'])
                )
            else:
                tire = Tires.objects.filter(
                    Q(size=transfer.values()[0]['size']) &
                    Q(brands_str=','.join(sorted(transfer.values()[0]['brands'])) if 
                        transfer.values()[0]['brands'] != None else None) &
                    Q(profiles_str=','.join(sorted(transfer.values()[0]['profiles'])) if 
                        transfer.values()[0]['profiles'] != None else None) &
                    Q(warehouse_id=transfer.values()[0]['sender'])
                )
            tire.update(pending_qty=0)
                    
            return Response({'updated': True, 'msg': 'Product {}'.format(status)})
            

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def come_in(self, request):
        """
        get base on the current date the incoming products and the count

        Args:
            request (dict): [request data]
        """
        dte = request.query_params.get('date')

        incoming = Products.objects.get_incoming_products(dte)

        return Response(incoming)

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def brands(self, request):
        return Response(serializers.serialize('json', Brands.objects.all_brands()))

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_brand(self, request):
        brand_name = request.data['body']['name']

        try:
            Brands.objects.create(name=brand_name)
            return Response({'added': True, 'msg': 'Brand added'})
        except Exception:
            return Response({'added': False, 'msg': 'Brand already exists'})

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def profiles(self, request):
        return Response(serializers.serialize('json', Profiles.objects.all_profiles()))

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_profile(self, request):
        name = request.data['body']['name']

        try:
            Profiles.objects.create(name=name)
            return Response({'added': True, 'msg': 'Profile added'})
        except Exception:
            return Response({'added': False, 'msg': 'Profile already exists'})

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def vehicles(self, request):
        return Response(serializers.serialize('json', Vehicule.objects.all_vehicles()))

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_vehicle(self, request):
        name = request.data['body']['name']

        try:
            Vehicule.objects.create(name=name)
            return Response({'added': True, 'msg': 'Vehicle added'})
        except Exception:
            return Response({'added': False, 'msg': 'Vehicle already exists'})


# Create your views here.
