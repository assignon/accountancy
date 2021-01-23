from rest_framework import serializers
from .models import Customers
# from dashboard.models import Appointments


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = "__all__"
