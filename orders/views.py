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

from orders.serializers import OrderSerializer
from .models import Customers, Orders, Payment

# Create your views here.


class OrderView(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def orders(self, request):
        """
        get base on the current date the orders and the count

        Args:
            request (dict): [request data]
        """
        dte = request.query_params.get('date')
        orders = Orders.objects.get_orders(dte)

        return Response(orders)

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def ongoing_payments(self, request):
        """
        get base on the ongoing payments

        Args:
            request (dict): [request data]
        """
        dte = request.query_params.get('date')
        # payments_dates = Payment.paymentDates_end(payment['id'])
        payments = Customers.objects.ongoing_payments(dte)

        return Response(payments)
