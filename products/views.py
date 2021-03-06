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
from .models import Products, Brands, Profiles, Tires

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
    @action(methods=['get'], detail=False)
    def products(self, request):
        """
        get all products count from DB

        Args:
            request (dict): [request data]
        """
        products = Products.objects.all_products()

        return Response(products)

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def filter_products(self, request):
        vehicle = request.query_params.get('vehicle')
        brands = json.loads(request.query_params.get('brands'))
        profiles = json.loads(request.query_params.get('profiles'))

        return Response(Products.objects.filter_products(vehicle, brands, profiles))

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def product_details(self, request):
        product_id = request.query_params.get('product_id')

        return Response(Products.objects.product_details(product_id))

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
    @action(methods=['get'], detail=False)
    def profiles(self, request):
        return Response(serializers.serialize('json', Profiles.objects.all_profiles()))


# Create your views here.
