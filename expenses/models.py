from django.db import models
from django.utils import timezone
from .managers import *


class Expenses(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    add_on = models.DateField(auto_now_add=True)
    objects = ExpensesManager()

    def __str__(self):
        return str(self.name)

    @staticmethod
    def daily_expenses_price(dte):
        """calculate the total daily expenses price

        Args:
            dte ([datetime]): [date]
        """
        expenses = Expenses.objects.filter(add_on=dte)
        total_expense = 0

        for expense in expenses.values():
            total_expense += expense['price']

        return total_expense
