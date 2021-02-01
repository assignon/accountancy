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
    @action(methods=['get'], detail=False)
    def get_user_data(self, request):
        user_id = request.query_params.get('user_id')

        user = User.objects.get(id=user_id)

        return Response({
            'email': user.email,
            'name': user.username
        })

    @csrf_exempt
    @action(methods=['put'], detail=False)
    def update_user_data(self, request):
        user_id = request.data['body']['user_id']
        email = request.data['body']['email']
        name = request.data['body']['name']
        current_password = request.data['body']['current_password']
        password = request.data['body']['password']

        user = User.objects.filter(id=user_id)

        if password == None:
            if User.objects.get(id=user_id).check_password(current_password):
                user.update(
                    username=name,
                    email=email,
                )

                return Response({'updated': True, 'msg': 'Email and name updated', 'user_id': user.values()[0]['id']})
            else:
                return Response({'updated': False, 'msg': 'Wrong password', 'user_id': user.values()[0]['id']})
        else:
            if user.check_password(current_password):
                user.update(
                    username=name,
                    email=email,
                )
                user.set_password(password)

                return Response({'updated': True, 'msg': 'Email and name updated', 'user_id': user.id})
            else:
                return Response({'updated': False, 'msg': 'Wrong password', 'user_id': user.id})

    @action(methods=['get'], detail=False)
    def signout(self, request):
        logout(request)
        return Response({'logout': True})
