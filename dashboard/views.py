# from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model

from django.contrib.auth.models import User
from django.http.response import HttpResponse
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
from django.conf import settings
from django.core.files import File
import shutil
import os
import sys
from pathlib import Path
import urllib.request
from django.contrib.auth.decorators import login_required

from dashboard.serializers import DashboardSerializer
from orders.models import Credentials
from products.models import Products

# Create your views here.


@login_required(login_url='/')
def backup(request):
    # download the sqlite DB to local disk
    db_path = settings.BASE_DIR+'/db.sqlite3'

    dbfile = File(open(db_path, "rb"))
    response = HttpResponse(dbfile, content_type="application/x-sqlite3")
    response['Content-Disposition'] = 'attachment; filename='+db_path
    response['Content-Length'] = dbfile.size

    return response


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    email = request.data['body']['email']  # can contain email or username
    password = request.data['body']['password']
    # get username and password count
    email_count = User.objects.filter(email=email).count()
    username_count = User.objects.filter(username=email).count()
    passsword_count = User.objects.filter(password=password).count()
    # check if user given email ans password exist in DB
    if email_count != 0 or username_count != 0:
        # verify if the user given password is correct
        try:
            currentUser = User.objects.get(email=email)
        except:
            currentUser = User.objects.get(username=email)

        if currentUser.check_password(password):
            # check if email is senden or username
            if email_count > 0:
                # get username
                username = User.objects.get(email=email).username
                user = authenticate(username=username, password=password)
            else:
                user = authenticate(
                    username=email, password=password)  # email=username
            # userToken(request, user)
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key,
                                 'id': token.user_id,
                                 'is_superuser': request.user.is_superuser,
                                 'username': request.user.username,
                                 'authenticate': True},
                                status=HTTP_200_OK)
            else:
                print('Gebruiker bestaat niet')
        else:
            passwordContext = {
                'authenticate': False,
                'msg': 'Wachtwoord onjuist',
            }
            return Response(passwordContext)
    else:
        emailContext = {
            'authenticate': False,
            'msg': 'Email or username onjuist'
        }
        return Response(emailContext)


class DashboardView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_warehouse(self, request):
        username = request.data['body']['username']
        email = request.data['body']['email'] if request.data['body']['email'] != None else 'None'
        password = request.data['body']['password']

        if request.user is not None:
            # check if user already exist
            user_exist = user = User.objects.filter(
                username=username).count()
            if user_exist == 0:
                user = User.objects.create_user(
                    username=username, email=email, password=password, is_superuser=0, is_staff=1)

                token, _ = Token.objects.get_or_create(user=user)

                return Response({
                    'msg': 'Warehouse added',
                    'created': True},
                    status=HTTP_200_OK)
            else:
                return Response({'msg': 'Warehouse already exist', 'created': False})

        else:
            return Response({'msg': 'Warehouse already exist', 'created': False})

    @csrf_exempt
    @action(methods=['put'], detail=False)
    def update_warehouse(self, request):
        username = request.data['body']['username']
        email = request.data['body']['email'] if request.data['body']['email'] != None else 'None'
        password = request.data['body']['password']
        whouse_id = request.data['body']['id']

        # check if user already exist
        whouse = User.objects.filter(id=whouse_id)
        get_warehouse = User.objects.get(id=whouse_id)
        if whouse.count() > 0:
            if username != None:
                whouse.update(
                    username=username
                )

            if email != None:
                whouse.update(
                    email=email
                )

            if password != None:
                get_warehouse.set_password(password)
                get_warehouse.save()

            return Response({
                'msg': 'Warehouse updated',
                'updated': True},
                status=HTTP_200_OK)
        else:
            return Response({'msg': 'Warehouse don t exists', 'updated': False})

    @csrf_exempt
    @action(methods=['delete'], detail=False)
    def delete_warehouse(self, request):
        whouse_id = request.query_params.get('id')
        User.objects.filter(id=whouse_id).delete()

        return Response({'msg': 'Warehouse deleted', 'deleted': True})

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_user_data(self, request):
        # get a warehouse base on id
        user_id = request.query_params.get('user_id')

        user = User.objects.get(id=user_id)

        return Response({
            'email': user.email,
            'name': user.username,
            'id': user.id,
            'added_on': user.date_joined.date(),
            'admin': user.is_superuser,
            'staff': user.is_staff,
            'active': user.is_active,
        })

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def get_warehouses(self, request):
        warehouse_arr = []

        warehouses = User.objects.all().values()
        for wh in warehouses:
            warehouse_arr.append(
                {
                    'name': wh['username'],
                    'id': wh['id'],
                    'email': wh['email'],
                    'su': wh['is_superuser'],
                    'added_on': wh['date_joined'].date()
                }
            )
        return Response(warehouse_arr)

    @csrf_exempt
    @action(methods=['put'], detail=False)
    def update_user_data(self, request):
        user_id = request.data['body']['user_id']
        email = request.data['body']['email']
        name = request.data['body']['name']
        current_password = request.data['body']['current_password']
        password = request.data['body']['password']

        user = User.objects.filter(id=user_id)
        get_user = User.objects.get(id=user_id)

        if password == None or password == "":
            if get_user.check_password(current_password):
                User.objects.filter(id=user_id).update(
                    username=name,
                    email=email,
                )

                return Response({'updated': True, 'msg': 'Email and name updated', 'user_id': user.values()[0]['id']})
            else:
                return Response({'updated': False, 'msg': 'Wrong password', 'user_id': user.values()[0]['id']})
        else:
            if get_user.check_password(current_password):
                user.update(
                    username=name,
                    email=email,
                )
                get_user.set_password(password)
                get_user.save()

                return Response({'updated': True, 'msg': 'Data updated', 'user_id': user.values()[0]['id']})
            else:
                return Response({'updated': False, 'msg': 'Wrong password', 'user_id': user.values()[0]['id']})

    # @csrf_exempt
    # @action(methods=['get'], detail=False)
    # def db_backup(self, request):
    #     # destination_folder = str(Path.home() / "Downloads/chicam_backups")
    #     # destination_path = str(destination_folder)+'/db.sqlite3'

    #     # if not os.path.exists(destination_folder):
    #     #     try:
    #     #         os.mkdir(destination_folder)
    #     #     except OSError:
    #     #         return Response(
    #     #             {
    #     #                 'created': False,
    #     #                 'msg': "Creation of the directory %s failed {}".format(destination_folder)
    #     #             }
    #     #         )

    #     # if os.path.exists(destination_path):
    #     #     os.remove(destination_path)
    #     #     try:
    #     #         shutil.copy(f'{settings.BASE_DIR}/db.sqlite3',
    #     #                     destination_path)
    #     #     except IOError as e:
    #     #         return Response(
    #     #             {
    #     #                 'created': False,
    #     #                 'msg': "Unable to copy file. {}".format(e)
    #     #             }
    #     #         )

    #     #     return Response(
    #     #         {
    #     #             'created': True,
    #     #             'msg': 'Backup created'
    #     #         }
    #     #     )
    #     #     # shutil.move(f'{settings.BASE_DIR}/db.sqlite3', downloads_path)
    #     # else:
    #     #     try:
    #     #         shutil.copy(f'{settings.BASE_DIR}/db.sqlite3',
    #     #                     destination_path)
    #     #     except IOError as e:
    #     #         return Response(
    #     #             {
    #     #                 'created': False,
    #     #                 'msg': "Unable to copy file. {}".format(e)
    #     #             }
    #     #         )

    #     #     return Response(
    #     #         {
    #     #             'created': True,
    #     #             'msg': 'Backup created'
    #     #         }
    #     #     )

    #     return response

    @action(methods=['get'], detail=False)
    def signout(self, request):
        logout(request)
        return Response({'logout': True})
