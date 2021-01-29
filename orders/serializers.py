from rest_framework import serializers
from .models import Customers, Payment
# from dashboard.models import Appointments


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
