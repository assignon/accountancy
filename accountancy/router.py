from rest_framework import routers
from dashboard.views import DashboardView
from orders.views import OrderView
from products.views import ProductView


router = routers.DefaultRouter()
router.register('dashboard', DashboardView)
router.register('order', OrderView)
router.register('product', ProductView)
