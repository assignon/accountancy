from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PaymentMethods)
admin.site.register(Payment)
admin.site.register(Orders)
admin.site.register(Credentials)
admin.site.register(Customers)
admin.site.register(ProductOrdered)
