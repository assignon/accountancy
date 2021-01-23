from rest_framework import serializers
from products.models import Products
# from dashboard.models import Appointments


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"
