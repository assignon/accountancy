from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import *


# @receiver(post_save, sender=Customers)
# def create_customer(sender, instance, created, **kwargs):
#     print('sender', sender)
#     print('instance', instance)
#     print('created', created)
#     print('kwargs', kwargs)
#     # #create credentials
#     # credentials = Credentials.objects.create()
#     # # create order
#     # order = Orders.objects.create()


# # @receiver(post_save, sender=Orders)
# # def create_customer(sebder, instance, **kwargs):
# #     pass


# # @receiver(post_save, sender=Orders)
# # def create_order(sebder, instance, created, **kwargs):
# #     pass
