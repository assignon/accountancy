from django.db import models
from datetime import datetime


def get_related(obj, parent, obj_id):
    """
    get related model data of a foreign key relation

    Args:
        obj ([model class]): [related model class]
        parent ([model class]): [model class with the foreign key]
        obj_id ([int]): [related model object id]

    Returns:
        [array]: [array with related object data]
    """
    related_arr = []
    for p in parent.values():
        related = obj.objects.filter(id=p[obj_id]).values()
        for r in related:
            related_arr.append(r)

    return related_arr


class CustomerManager(models.Manager):
    def get_orders(self, dte=None):
        from products.models import Products
        from .models import Customers
        """
        get orders base on the give date

        Args:
            dte ([date], optional): [current date if none else give date]. Defaults to None.

        Returns:
            [obj]: [products data]
        """
        current_date = datetime.now().date()

        if dte == None:
            # get products of the current date
            orders = self.select_related().filter(
                add_on=current_date.date())

            return {
                'orders': orders.values(),
                # 'tire': [get_related(Tires, id=product['tire_id']) for product in added_products],
                'products': get_related(Products, orders, 'product_id'),
                'count': orders.count()
            }
        else:
            # get products base on give date
            orders = self.select_related().filter(
                add_on=dte)

            return {
                'orders': orders.values(),
                'products': get_related(Products, orders, 'tire_id'),
                'count': orders.count()
            }

    def ongoing_payments(self, dte=None, lmit=None):
        from .models import Customers, Credentials, Payments, PaymentMethods
        current_date = datetime.now().date()
        current_dates_payments = []
        # querysets
        customers = Customers.select_related.all()
        credential = get_related(Credentials, customers, 'credential_id')
        payments = get_related(Payments, customers, 'payment_id')
        payment_methods = get_related(PaymentMethods, payments, 'method_id')

        if dte == None:
            # get customer who are paying on the current day
            for payment in payments:
                if current_date in Payments.paymentDates_end(payment['id'])['paying_dates']:
                    current_dates_payments.append(payment)[:10]

            return {
                'credentials': credential,
                'payments': current_dates_payments,
                'methods': payment_methods
            }
        else:
            return {
                'credentials': credential,
                'payments': payments,
                'methods': payment_methods
            }
            # # get all ongoing payment with limit
            # pass
            # if lmit == None:
            #     # get all the ongoing payments
            #     pass
            # else:
            #     # get the ongoing payment base on the given limit
            #     pass
