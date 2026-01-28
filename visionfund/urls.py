"""
URL configuration for visionfund project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.defaults import permission_denied

handler403 = permission_denied

urlpatterns = [
    path('admin/', admin.site.urls),

    path('customers/', include('customers.urls')),
    path('savings/', include('savings.urls')),
    path('loans/', include('loans.urls')),
    path('accounting/', include('accounting.urls')),
    path('reports/', include('reports.urls')),
    path('accounts/', include('accounts.urls')),
]
