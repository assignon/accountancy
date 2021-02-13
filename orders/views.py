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

from orders.serializers import OrderSerializer, PaymentSerializer, CustomerSerializer
from .models import Customers, Orders, Payment

# Create your views here.


class OrderView(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_order(self, request):
        """
        create new order

        Args:
            request (dict): [request data]
        """
        # dte = request.query_params.get('date')
        data = {
            # customer data
            'name': request.data['body']['name'],
            'email': request.data['body']['email'],
            'address': request.data['body']['address'],
            'tel_number': request.data['body']['tel_number'],
            'times': request.data['body']['times'],
            'start': request.data['body']['start'],
            # order data
            'ordered_products': request.data['body']['ordered_products'],
            # payment data
            'method': request.data['body']['method'],
            'pay_in': request.data['body']['pay_in'],
            'payment_interval': request.data['body']['payment_interval'],
        }

        return Response(Orders.objects.create_order(**data))

    @csrf_exempt
    @action(methods=['delete'], detail=False)
    def remove_order(self, request):
        """
        remove order

        Args:
            request (dict): [request data]
        """
        order_id = request.query_params.get('order_id')
        Orders.objects.remove_order(order_id)

        return Response({'remove': True})

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
        get base on the date ongoing payments

        Args:
            request (dict): [request data]
        """
        dte = datetime.strftime(datetime.now().date(), '%Y-%m-%d') if request.query_params.get(
            'date') == None else request.query_params.get('date')
        limit = request.query_params.get('limit')
        # payments_dates = Payment.paymentDates_end(payment['id'])
        payments = Customers.objects.ongoing_payments(dte, limit)

        return Response(payments)

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def payments(self, request):
        """
        get base all ongoing payments

        Args:
            request (dict): [request data]
        """
        limit = request.query_params.get('limit')

        payments = Customers.objects.all_payments(limit)

        return Response(payments)

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def order_details(self, request):
        """
        get base on the customer id order details

        Args:
            request (dict): [request data]
        """
        customer_id = request.query_params.get('customerId')
        order = Customers.objects.customer_orders(customer_id)

        return Response(order)

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def payment_details(self, request):
        """
        get base on the customer id order details

        Args:
            request (dict): [request data]
        """
        customer_id = request.query_params.get('customerId')
        payment = Customers.objects.customer_ongoing_payment(customer_id)

        return Response(payment)


class PaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def payment_methods(self, request):
        """
        get the available payment methods

        Args:
            request (dict): [request data]
        """
        paymentmethods = Payment.objects.get_payment_methods()

        return Response(paymentmethods)


class CustomerView(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def credentials_form_auto_fill(self, request):
        email = request.query_params.get('email')

        return Response(Customers.objects.get_credentials_by_email(email))
