from django.db import models
from datetime import datetime
from django.core import serializers
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


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


def get_prefetch_related(parent):
    """
    get related model data of a many to many key relation

    Args:
        related_field ([model class]): [related field name in model class]
        parent ([model class]): [model class with the many to many key]

    Returns:
        [array]: [array with related object data]
    """
    related_arr = None

    for p in parent:
        related_arr = p

    return related_arr


class OrdersManager(models.Manager):
    def create_order(self, **kwargs):
        from orders.models import Customers, Payment, PaymentMethods, ProductOrdered, Tires, Credentials
        from products.models import Vehicule

        # get payment method
        method = PaymentMethods.objects.get(name=kwargs['method'])
        # create order
        order = self.prefetch_related().create()
        order.save()
        for product in kwargs['ordered_products']:
            # get tire
            try:
                global vehicle
                vehicle = Vehicule.objects.get(name=product['vehicule'])
            except ObjectDoesNotExist:
                global vehucle
                vehicle = Vehicule.objects.create(name=product['vehicule'])

            brands_arr = ','.join(sorted(product['brand'])) if len(
                product['brand']) > 0 else "{}".format(sorted(product['brand'][0]))
            profile_arr = ','.join(sorted(product['profile'])) if len(
                product['profile']) > 0 else '{}'.format(sorted(product['profile'][0]))

            tire = Tires.objects.get(
                Q(size=product['name']) &
                Q(profiles_str=profile_arr) &
                Q(brands_str=brands_arr)
            )
            # create ordered products
            # try:
            ordered_products = ProductOrdered.objects.create(
                product=tire, quantity=product['qty'])
            order.product_ordered.add(ordered_products)
            # update tire quantity
            tire_update = Tires.objects.filter(
                Q(size=product['name']) &
                Q(profiles_str=profile_arr) &
                Q(brands_str=brands_arr)
            )
            if int(tire.quantity) > 0:
                new_quantity = int(tire.quantity) - int(product['qty'])
                tire_update.update(quantity=new_quantity)
            else:
                tire_update.update(quantity=0)
            # except Exception:
            #     return {'create': False, 'msg': 'ordered product(s) quantity must be > 0'}

        # create payment
        payment_obj = Payment.objects.create(
            method=method,
            pay_in=kwargs['pay_in'],
            payment_interval=kwargs['payment_interval'] if kwargs['pay_in'] != 'Once' else 'daily',
        )
        payment_obj.save()
        # create credential
        credentials = Credentials.objects.create(
            name=kwargs['name'],
            email=kwargs['email'],
            address=kwargs['address'],
            tel_number=kwargs['tel_number']
        ).save()
        # create customer
        customer = Customers.objects.create(
            credential=credentials,
            order=order,
            payment=payment_obj,
            times=kwargs['times'] if kwargs['pay_in'] != 'Once' else 0,
            start=kwargs['start']
        )

        return {'created': True, 'msg': 'Order places', 'order_id': customer.pk}

    def remove_order(self, order_id):
        from orders.models import Customers

        order = self.prefetch_related().get(id=order_id)

        # remove all ordered products
        order.product_ordered.all().delete()
        # remove customer and order
        Customers.objects.filter(order_id=order_id).delete()

        return 'Order removed'

    def get_orders(self, dte=None, limit=None):
        from products.models import Vehicule
        from orders.models import Customers, Payment, PaymentMethods, ProductOrdered, Tires, Orders
        """
        get orders base on the give date

        Args:
            dte ([date], optional): [current date if none else give date]. Defaults to None.

        Returns:
            [obj]: [products data]
        """
        current_date = datetime.now().date()
        orders_arr = []

        if dte == None:
            # get products of the current date
            orders = self.prefetch_related().filter(
                order_on=current_date) if limit == None else self.prefetch_related().filter(
                order_on=current_date)[:limit]

            # get credentials and orders
            for order in orders.values():
                customer = Customers.objects.get_customer(
                    order_id=order['id'])
                payment = Payment.objects.filter(id=customer.payment_id)

                ordered_products = ProductOrdered.objects.filter(
                    orders__id=order['id'])

                payment_data = {
                    'method': get_related(PaymentMethods, payment, 'method_id'),
                    'pay_in': payment.values()[0]['pay_in'],
                    'payment_interval': payment.values()[0]['payment_interval'],
                    'times': customer.times,
                    'start': customer.start
                }

                orders_arr.append({
                    'order': order,
                    'credentials': Customers.objects.get_credentials(
                        order_id=order['id']),
                    'payment': payment_data,
                    'paying': Orders.paying(order['id']),
                    'ordered_products': [
                        {
                            'ordered_product': p_d,
                            'product': Tires.objects.filter(id=p_d['product_id']).values(),
                            'vehicule': get_related(Vehicule, Tires.objects.filter(id=p_d['product_id']), 'vehicule_id'),
                            'brands': [brand for brand in get_prefetch_related(Tires.objects.filter(id=p_d['product_id'])).brands.all().values()],
                            'profiles':  [profile for profile in get_prefetch_related(Tires.objects.filter(id=p_d['product_id'])).profiles.all().values()],
                        }
                        for p_d in ordered_products.values()
                    ]
                })

            return {
                'order': orders_arr,
                'count': orders.count()
            }

        else:
            # get products base on give date
            orders = self.prefetch_related().filter(
                order_on=dte) if limit == None else self.prefetch_related().filter(
                order_on=dte)[:limit]

            for order in orders.values():
                customer = Customers.objects.get_customer(
                    order_id=order['id'])
                payment = Payment.objects.filter(id=customer.payment_id)

                ordered_products = ProductOrdered.objects.filter(
                    orders__id=order['id'])

                payment_data = {
                    'method': get_related(PaymentMethods, payment, 'method_id'),
                    'pay_in': payment.values()[0]['pay_in'],
                    'payment_interval': payment.values()[0]['payment_interval'],
                    'times': customer.times,
                    'start': customer.start
                }

                orders_arr.append({
                    'order': order,
                    'credentials': Customers.objects.get_credentials(
                        order_id=order['id']),
                    'payment': payment_data,
                    'paying': Orders.paying(order['id']),
                    'ordered_products': [
                        {
                            'ordered_product': p_d,
                            'product': Tires.objects.filter(id=p_d['product_id']).values(),
                            'vehicule': get_related(Vehicule, Tires.objects.filter(id=p_d['product_id']), 'vehicule_id'),
                            'brands': [brand for brand in get_prefetch_related(Tires.objects.filter(id=p_d['product_id'])).brands.all().values()],
                            'profiles':  [profile for profile in get_prefetch_related(Tires.objects.filter(id=p_d['product_id'])).profiles.all().values()],
                        }
                        for p_d in ordered_products.values()
                    ]
                })

            return {
                'order': orders_arr,
                'count': orders.count()
            }


class PaymentManager(models.Manager):
    def get_payment_methods(self):
        from .models import PaymentMethods

        # payments = self.select_related().all()
        payment_methods = PaymentMethods.objects.all()
        payment_methos_arr = []

        for payment_method in payment_methods.values():
            # payment_method = PaymentMethods.objects.get(
            #     id=payment['method_id'])
            payment_methos_arr.append({
                'method': payment_method['name'],
            })

        return payment_methos_arr

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

    def get_customer(self, **kwargs):
        try:
            customer = self.select_related().get(**kwargs)
            return customer
        except ObjectDoesNotExist:
            return False

    def get_credentials(self, **kwargs):
        from orders.models import Credentials

        customer = self.select_related().get(**kwargs)
        credentials = Credentials.objects.get(id=customer.credential_id)

        return {
            'id': credentials.id,
            'customer_id': customer.id,
            'name': credentials.name,
            'email': credentials.email,
            'address': credentials.address,
            'tel_number': credentials.tel_number,
        }

    def get_credentials_by_email(self, email):
        from orders.models import Credentials

        credentials = Credentials.objects.filter(email__icontains=email)
        if credentials.count() > 0:
            return {'founded': True, 'credentials': credentials.values()}
        else:
            return {'founded': False, 'credentials': None}

    def customer_orders(self, customerid):
        from products.models import Products, Vehicule, Tires
        from orders.models import Orders, Credentials, Payment, PaymentMethods, ProductOrdered
        """
        get orders by customer id

        Args:
            customerid [id]: customer id

        Returns:
            [obj]: [products data]
        """
        customer = self.select_related().filter(id=customerid)
        products_ordered_arr = []

        # get orders
        order = Orders.objects.get(
            id=customer.values()[0]['order_id'])
        print('ord', order.id)
        payment = Payment.objects.filter(id=customer.values()[0]['payment_id'])
        # payment_id = payment.values()[0]['id']
        products_ordered = order.product_ordered.all()

        for product_ordered in products_ordered.values():
            products = Tires.objects.filter(
                id=product_ordered['product_id'])
            products_ordered_arr.append(
                {
                    'ordered_product': product_ordered,
                    'products': products.values(),
                    'profiles': get_prefetch_related(products).profiles.all().values(),
                    'brands': get_prefetch_related(products).brands.all().values(),
                    'vehicule': get_related(Vehicule, products, 'vehicule_id'),
                }
            )

        return {
            'order': {
                'order_on': order.order_on,
                'order_at': order.order_at
            },
            'customer': customer.values(),
            'credential': get_related(Credentials, customer, 'credential_id'),
            'products':  products_ordered_arr,
            'payment': payment.values(),
            'paying': Orders.paying(order.id),
            'method': get_related(PaymentMethods, payment, 'method_id'),
            'payment_helper': {
                'paymentDates_end': Payment.paymentDates_end(customer.values()[0]['id']),
                'paying_in_terms': Payment.paying_in_terms(customer.values()[0]['id']),
                'completed': Payment.completed(customer.values()[0]['id'])
            }
        }

    def customer_ongoing_payment(self, paymentid):
        from .models import Credentials, Payment, PaymentMethods, Orders
        # querysets
        # customers = self.select_related().filter(credential_id=paymentid)
        customers = self.select_related().filter(payment_id=paymentid)
        print('cuussst', customers.values()[0]['order_id'])
        order = Orders.objects.get(id=customers.values()[0]['order_id'])
        credential = get_related(Credentials, customers, 'credential_id')
        payments = get_related(Payment, customers, 'payment_id')
        payment_methods = PaymentMethods.objects.filter(
            id=payments[0]['method_id'])

        return {
            'customer': customers.values(),
            'credentials': credential,
            'payments': payments,
            'methods': payment_methods.values(),
            'paying_term': Payment.paying_in_terms(customers.values()[0]['id']),
            'paying': Orders.paying(order.id),
            'payment_dates': Payment.paymentDates_end(customers.values()[0]['id'])
        }

    def ongoing_payments(self, dte, limit):
        from .models import PaymentMethods, Payment, Credentials, Customers

        customer_payments = []
        customer_payment_method = []
        credentials = []
        # querysets
        # payments = Payment.objects.all(
        # )[:int(limit)] if int(limit) != 0 else Payment.objects.all()

        customers = Customers.objects.all(
        )[:int(limit)] if int(limit) != 0 else Customers.objects.all()

        # get customer who are paying on the current day
        # for payment in payments.values():
        for customer in customers.values():
            payments_dates = Payment.paymentDates_end(customer['id'])
            payment = Payment.objects.get(id=customer['payment_id'])
            # dte_obj = datetime.strptime(dte, '%Y-%m-%d')

            for dates in payments_dates['paying_dates']:
                if dte == datetime.strftime(dates, '%Y-%m-%d'):
                    payment_method = Payment.objects.filter(
                        id=customer['payment_id'])

                    customer_payments.append(
                        {
                            'id': customer['payment_id'],
                            'customer_id': customer['id'],
                            'method_id': payment.method_id,
                            'pay_in': payment.pay_in,
                            'payment_interval': payment.payment_interval,
                            'start': customer['start'],
                            'times': customer['times'],
                            'payment_dates': payments_dates['paying_dates'],
                            # get payments methods
                            'methods': get_related(
                                PaymentMethods, payment_method, 'method_id'),
                            # get customer credentials
                            'customer': Credentials.objects.filter(id=customer['credential_id']).values()
                        }
                    )

        return {
            'payments': customer_payments,
            'count': len(customer_payments),
        }

    def all_payments(self, limit):
        from .models import PaymentMethods, Payment, Credentials, Customers

        customer_payments = []
        # querysets
        customers = Customers.objects.all(
        )[:int(limit)] if int(limit) != 0 else Customers.objects.all()

        for customer in customers.values():
            payments_dates = Payment.paymentDates_end(customer['id'])
            payment_method = Payment.objects.filter(id=customer['payment_id'])
            payment = Payment.objects.get(id=customer['payment_id'])
            print('payyy', payment.pay_interval)

            customer_payments.append(
                {
                    'id': customer['payment_id'],
                    'method_id': payment.method_id,
                    'pay_in': payment.pay_in,
                    'payment_interval': payment.payment_interval,
                    'start': customer['start'],
                    'times': customer['times'],
                    'payment_dates': payments_dates['paying_dates'],
                    # get payments methods
                    'methods': get_related(
                        PaymentMethods, payment_method, 'method_id'),
                    # get customer credentials
                    'customer': get_related(
                        Credentials, customers, 'credential_id')
                }
            )

        return {
            # 'customers': credentials,
            'payments': customer_payments,
            # 'methods': customer_payment_method,
            'count': len(customer_payments),
        }
