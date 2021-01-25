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


class OrdersManager(models.Manager):
    def get_orders(self, dte=None, limit=None):
        from products.models import Products
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
            orders = self.prefetch_related().filter(
                order_on=current_date) if limit == None else self.prefetch_related().filter(
                order_on=current_date)[:limit]

            return {
                'orders': orders.values(),
                # 'tire': [get_related(Tires, id=product['tire_id']) for product in added_products],
                # 'products': get_related(Products, orders, 'product_id'),
                'count': orders.count()
            }
        else:
            # get products base on give date
            orders = self.prefetch_related().filter(
                order_on=dte) if limit == None else self.prefetch_related().filter(
                order_on=dte)[:limit]

            return {
                'orders': orders.values(),
                # 'products': get_related(Products, orders, 'tire_id'),
                'count': orders.count()
            }


class PaymentManager(models.Manager):
    pass
    # def ongoing_payments(self, dte=None):
    #     from .models import PaymentMethods, Payment

    #     current_date = datetime.now().date()
    #     current_dates_payments = []
    #     # querysets
    #     payments = self.select_related().all()
    #     payment_methods = get_related(PaymentMethods, payments, 'method_id')

    #     if dte == None:
    #         # get customer who are paying on the current day
    #         for payment in payments.values():
    #             payments_dates = Payment.paymentDates_end(payment['id'])
    #             if current_date in payments_dates['paying_dates']:
    #                 current_dates_payments.append(payment)[:10]

    #         return {
    #             'payments': current_dates_payments,
    #             'methods': payment_methods
    #         }
    #     else:
    #         return {
    #             'payments': payments,
    #             'methods': payment_methods
    #         }


class CustomerManager(models.Manager):
    def customer_orders(self, customerid):
        from products.models import Products
        from orders.models import Orders, Credentials
        """
        get orders base on the give date

        Args:
            dte ([date], optional): [current date if none else give date]. Defaults to None.

        Returns:
            [obj]: [products data]
        """
        customer = self.select_related().filter(
            order_id=customerid)
        # get orders
        orders = get_related(Orders, customer, 'order_id'),

        return {
            'orders': orders,
            'credential': get_related(Credentials, customer, 'credential_id'),
            'products': get_related(Products, orders, 'product_id'),
            'count': orders.count()
        }

    def customer_ongoing_payment(self, customerid):
        from .models import Credentials, Payments, PaymentMethods
        # querysets
        customers = self.select_related().filter(id=customerid)
        credential = get_related(Credentials, customers, 'credential_id')
        payments = get_related(Payments, customers, 'payment_id')
        payment_methods = get_related(PaymentMethods, payments, 'method_id')

        return {
            'credentials': credential,
            'payments': payments,
            'methods': payment_methods
        }

    def ongoing_payments(self, dte=datetime.now().date(), limit=None):
        from .models import PaymentMethods, Payment, Credentials

        customer_payments = []
        customer_payment_method = []
        credentials = []
        # querysets
        payments = Payment.objects.all(
        ) if limit == None else Payment.select_related().all()[:limit]

        # get customer who are paying on the current day
        for payment in payments.values():
            payments_dates = Payment.paymentDates_end(payment['id'])
            # dte_obj = datetime.strptime(dte, '%Y-%m-%d')

            for dates in payments_dates['paying_dates']:
                if dte == datetime.strftime(dates, '%Y-%m-%d'):
                    payment_method = Payment.objects.filter(id=payment['id'])
                    customer_payments.append(
                        {
                            'id': payment['id'],
                            'method_id': payment['method_id'],
                            'pay_in': payment['pay_in'],
                            'payment_interval': payment['payment_interval'],
                            'start': payment['start'],
                            'times': payment['times'],
                            'payment_dates': payments_dates['paying_dates']
                        }
                    )
                    # get payments methods
                    customer_payment_method.extend(get_related(
                        PaymentMethods, payment_method, 'method_id'))
                    # get customer credentials
                    customers = self.select_related().filter(
                        payment_id=payment['id'])
                    credentials.extend(get_related(
                        Credentials, customers, 'credential_id'))

        return {
            'customers': credentials,
            'payments': customer_payments,
            'methods': customer_payment_method,
            'count': len(customer_payments)
        }
