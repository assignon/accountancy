from rest_framework import routers
from dashboard.views import DashboardView
from orders.views import OrderView, PaymentView, CustomerView
from products.views import ProductView
from expenses.views import ExpensesView


router = routers.DefaultRouter()
router.register('dashboard', DashboardView)
router.register('order', OrderView)
router.register('product', ProductView)
router.register('payment', PaymentView)
router.register('customer', CustomerView)
router.register('expense', ExpensesView)
