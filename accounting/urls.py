from django.urls import path
from . import views
from .views import daily_cash_summary

urlpatterns = [
    path('daily-summary/', daily_cash_summary, name='daily_summary'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]