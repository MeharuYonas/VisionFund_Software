from django.urls import path
from . import views

urlpatterns = [
    path(
        'repayment-mortgage/',
        views.loan_repayment_mortgage,
        name='loan_repayment_mortgage'
    ),
    path(
        'repayment-mortgage/csv/',
        views.loan_repayment_mortgage_csv,
        name='loan_repayment_mortgage_csv'
    ),
]
