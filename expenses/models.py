from django.db import models
from django.db.models import Q
from django.utils import timezone
from .managers import *
from django.contrib.auth.models import User


class Expenses(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    add_on = models.DateField(auto_now_add=True)
    warehouse_id = models.IntegerField(default=1)  # user id
    objects = ExpensesManager()

    def __str__(self):
        return str(self.name)

    @staticmethod
    def is_su(user_id):
        user = User.objects.get(id=user_id)

        return True if user.is_superuser else False

    @staticmethod
    def daily_expenses_price(dte, user_id):
        """calculate the total daily expenses price

        Args:
            dte ([datetime]): [date]
        """
        expenses = Expenses.objects.filter(add_on=dte) if user_id == 0 else Expenses.objects.filter(
            Q(add_on=dte) & Q(warehouse_id=user_id))
        total_expense = 0

        for expense in expenses.values():
            total_expense += expense['price']

        return total_expense
    
    @staticmethod
    def monthly_expense_price(user_id):
        """get expense of the current month

        Args:
            mth (date str): [current date]
            user_id (int): [logged user id]
        """
        current_month = datetime.now().date().month
        month_expense = 0
        #get monthly expenses
        expenses = Expenses.objects.filter(add_on__month=current_month) if user_id == 0 else Expenses.objects.filter(
            Q(add_on__month=current_month) & Q(warehouse_id=user_id))
        
        for expense in expenses.values():
            month_expense += expense['price']

        return month_expense
