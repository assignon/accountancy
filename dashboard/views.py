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

from dashboard.serializers import DashboardSerializer
from orders.models import Credentials
from products.models import Products

# Create your views here.


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    email = request.data['body']['email']
    password = request.data['body']['password']
    # get username and password count
    email_count = User.objects.filter(email=email).count()
    passsword_count = User.objects.filter(password=password).count()
    # check if user given email ans password exist in DB
    if email_count != 0:
        # verify if the user given password is correct
        currentUser = User.objects.get(email=email)
        if currentUser.check_password(password):
            # get username
            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)
            # userToken(request, user)
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key,
                                 'id': token.user_id,
                                 'is_superuser': request.user.is_superuser,
                                 'authenticate': True},
                                status=HTTP_200_OK)
            else:
                print('Gebruiker bestaat niet')
        else:
            passwordContext = {
                'authenticate': False,
                'ww': password,
                'msg': 'Wachtwoord onjuist',
            }
            return Response(passwordContext)
    else:
        emailContext = {
            'authenticate': False,
            'msg': 'Email onjuist'
        }
        return Response(emailContext)


class DashboardView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def products(self, request):
        """
        get all products count from DB

        Args:
            request (dict): [request data]
        """
        pass

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def come_in(self, request):
        """
        get base on the current date the incoming products and the count

        Args:
            request (dict): [request data]
        """
        pass

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def day_orders(self, request):
        """
        get base on the current date the orders and the count

        Args:
            request (dict): [request data]
        """
        pass

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def ongoing_payments(self, request):
        """
        get base on the ongoing payments

        Args:
            request (dict): [request data]
        """
        pass
