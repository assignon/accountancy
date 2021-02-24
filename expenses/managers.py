from django.db import models
from datetime import datetime
from django.core import serializers
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


class ExpensesManager(models.Manager):

    def add_expenses(self, **kwargs):
        new_expense = self.get_queryset().create(
            name=kwargs['name'], price=kwargs['price'], warehouse_id=kwargs['user_id'])

        return {'added': True, 'expense_id': new_expense.pk}

    def get_daily_expenses(self, dte, user_id):
        from .models import Expenses

        expenses = self.get_queryset().filter(add_on=dte) if user_id == 0 else self.get_queryset(
        ).filter(Q(add_on=dte) & Q(warehouse_id=user_id))

        return {
            'expenses': expenses.values(),
            'count': expenses.count(),
            'daily_total': Expenses.daily_expenses_price(dte, user_id)
        }
