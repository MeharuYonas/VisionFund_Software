from django.urls import path
from . import views

urlpatterns = [
    path('', views.saving_list, name='saving_list'),
    path('create/', views.saving_create, name='saving_create'),
    path('withdraw/<int:pk>/', views.saving_withdraw, name='saving_withdraw'),
]
