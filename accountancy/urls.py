"""accountancy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
# from django.views.generic import TemplateView
# from django.views import defaults as default_views
# from django.contrib.auth.views import logout
from .router import router
from dashboard import views as dash_view
from django.conf.urls import url
from django.views.generic import TemplateView
from accountancy import views

urlpatterns = [

    # path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/signin/', dash_view.signin),
    path('backup/', dash_view.backup),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    # frontend urls
    path('', views.login, name='Login'),
    path('orders/', views.orders, name='orders'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
    path('settings/', views.settings, name='settings'),
    path('expenses/', views.expenses, name='expenses'),
    path('transfers/', views.transfers, name='transfers'),
    path('warehouses/', views.warehouses, name='warehouses'),

] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT,
)
