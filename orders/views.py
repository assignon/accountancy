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
from django.core.exceptions import ObjectDoesNotExist
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
from .models import Customers, Orders, Payment, PaymentMethods, Payment_status, ProductOrdered
from products.models import Tires, Vehicule

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
            'user_id': request.data['body']['user_id'],
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
    
    # @csrf_exempt
    # @action(methods=['get'], detail=False)
    # def productHas_enoughQty(self, request):

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
        user_id = request.query_params.get('user_id')
        pagination = int(request.query_params.get('pagination'))
        limit = int(request.query_params.get('limit')
                    ) if request.query_params.get('limit') != None else None
        orders = Orders.objects.get_orders(user_id, pagination, dte, limit)

        return Response(orders)
    
    @csrf_exempt
    @action(methods=['get'], detail=False)
    def print_order(self, request):
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')
        user_id = request.query_params.get('user_id')
        
        return Response(Orders.objects.print_sales(user_id, start_date, end_date))

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def search_order(self, request):
        customer_name = request.query_params.get('customer_name')
        whouse_id = request.query_params.get('user_id')

        return Response(Orders.objects.search_order(customer_name, whouse_id))

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
        limit = int(request.query_params.get('limit'))
        warehouse_id = int(request.query_params.get('user_id'))
        su_id = int(request.query_params.get('su_id'))
        pagination = int(request.query_params.get('pagination'))
        # payments_dates = Payment.paymentDates_end(payment['id'])
        payments = Customers.objects.ongoing_payments(
            dte, limit, warehouse_id, su_id, pagination)

        return Response(payments)

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def payments(self, request):
        """
        get base all ongoing payments

        Args:
            request (dict): [request data]
        """
        limit = int(request.query_params.get('limit'))
        warehouse_id = int(request.query_params.get('user_id'))
        su_id = int(request.query_params.get('su_id'))
        pagination = int(request.query_params.get('pagination'))

        payments = Customers.objects.all_payments(
            limit, warehouse_id, su_id, pagination)

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

    @csrf_exempt
    @action(methods=['put'], detail=False)
    def update_payment_status(self, request):
        payment_id = Customers.objects.get(
            id=request.data['body']['customer_id'])
        # payment_date = request.data['body']['payment_date']
        # payment_date = datetime.strftime(datetime.now().date(), '%Y-%m-%d')
        order_id =  request.data['body']['order_id']
        payment_date = request.data['body']['payment_date']
        employee_name = request.data['body']['employee_name']
        update_custom_price = request.data['body']['update_custom_price']
        custome_payment = request.data['body']['custome_payment'] if request.data['body']['custome_payment'] != None else 0
        new_value = request.data['body']['new_value']  # boolean
        
        # paymentDetails[0].paying_term-ps.custome_payment

        pstatus = Payment_status.objects.filter(
            Q(payment__id=payment_id.payment_id) &
            Q(payment_date=payment_date)
        )
        # print('tteeerrrmmmsss',payment_id.paying_term)
        print('custom pay',custome_payment)
        print('custom price paid', pstatus.values()[0]['custome_payment'])
        print('paying termssss', Payment.paying_in_terms(payment_id.payment_id))
        print('resstttee', int(Payment.paying_in_terms(payment_id.payment_id))-int(custome_payment))
        
        total_custom_pay = pstatus.values()[0]['custome_payment'] # total custom price already paid by the customer
        paying_in_terms = Payment.paying_in_terms(payment_id.payment_id) # price customer gonna pay by term
        remaining_custome_price = int(Payment.paying_in_terms(payment_id.payment_id))-int(total_custom_pay) # remaing custom price after pay
        
        if int(custome_payment) > int(paying_in_terms) or int(custome_payment) < 0:
            return Response({'updated': False, 'msg': 'The order remaining price ({}) cannot be less than the custom priceee {} - {}'.format(remaining_custome_price, paying_in_terms, custome_payment)})
        elif int(custome_payment) > int(remaining_custome_price) or int(custome_payment) < 0:
            return Response({'updated': False, 'msg': 'The order remaining price ({}) cannot be less than the custom priceee'.format(remaining_custome_price)})
        
        # print([pstatus])
        if new_value:
            updated_custom_payment = pstatus.values()[0]['custome_payment']+int(custome_payment)
        else:
            updated_custom_payment = 0
        pstatus.update(payed=new_value, employee_name=employee_name, custome_payment=updated_custom_payment)
        
        ## update tire qty after payment received
        # get payment interval
        if update_custom_price == False:
            payment = Payment.objects.get(id=payment_id.payment_id)
            # get products ordered
            product_ordered = ProductOrdered.objects.filter(orders__id=order_id)
            
            if payment.pay_in == 'once':
                for po in product_ordered.values():
                    tire = Tires.objects.filter(id=po['product_id'])
                    # update tire qty
                    if int(tire.values()[0]['quantity']) > 0:
                        new_quantity = int(
                            tire.values()[0]['quantity']) - int(po['quantity'])
                        tire.update(quantity=new_quantity)
                    else:
                        tire.update(quantity=0)
            else:
                # if the customer is paying in terms
                ps_arr = [] #payment status payed array
                payment_status = payment.payment_status.all()
                for ps in payment_status.values():
                    ps_arr.append(ps['payed'])
                # check if all payment terms are been paid
                if False not in ps_arr:
                    for po in product_ordered.values():
                        tire = Tires.objects.filter(id=po['product_id'])
                    # update tire qty
                    if int(tire.values()[0]['quantity']) > 0:
                        new_quantity = int(
                            tire.values()[0]['quantity']) - int(po['quantity'])
                        tire.update(quantity=new_quantity)
                    else:
                        tire.update(quantity=0)

        return Response({'updated': True, 'msg': 'payment status updated'})

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_payment_method(self, request):
        method_name = request.data['body']['name']
        # add new payment method
        try:
            PaymentMethods.objects.create(name=method_name)
            return Response({'added': True, 'msg': 'Payment method added'})
        except Exception:
            return Response({'added': False, 'msg': 'This payment method already exists'})


class CustomerView(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def credentials_form_auto_fill(self, request):
        email = request.query_params.get('email')

        return Response(Customers.objects.get_credentials_by_email(email))
