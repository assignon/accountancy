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

from expenses.serializers import ExpensesSerializer
from .models import Expenses

# Create your views here.


class ExpensesView(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    @action(methods=['post'], detail=False)
    def new_expense(self, request):
        req = request.data['body']
        data = {
            'name': req['name'],
            'price': req['price'],
            'user_id': int(req['user_id'])
        }

        return Response(Expenses.objects.add_expenses(**data))

    @csrf_exempt
    @action(methods=['get'], detail=False)
    def expenses(self, request):
        dte = datetime.strftime(datetime.now().date(), '%Y-%m-%d') if request.query_params.get(
            'date') == None else request.query_params.get('date')
        user_id = int(request.query_params.get('user_id'))

        return Response(Expenses.objects.get_expenses(dte, user_id))
