from django.urls import path
from . import views

urlpatterns = [
    # Normal Views
    path('savings/', views.savings_report, name='savings_report'),
    path('loans/', views.loan_portfolio, name='loan_portfolio'),
    path('par/', views.par_report, name='par_report'),
    path('daily/', views.daily_report, name='daily_report'),
    path('monthly/', views.monthly_report, name='monthly_report'),
    path('cash-reconciliation/', views.cash_reconciliation, name='cash_reconciliation'),
    path('audit-trail/', views.audit_trail_view, name='audit_trail'),
    path('dashboard/', views.reports_dashboard, name='reports_dashboard'),

    # CSV Exports
    path('export/savings/csv/', views.export_savings_csv, name='export_savings_csv'),
    path('daily/csv/', views.daily_report_csv, name='daily_report_csv'),
    path('monthly/csv/', views.monthly_report_csv, name='monthly_report_csv'),
    path('cash-reconciliation/csv/', views.cash_reconciliation_csv, name='cash_reconciliation_csv'),
    path('audit-trail/csv/', views.audit_trail_csv, name='audit_trail_csv'),

    # PDF Exports
    path('daily/pdf/', views.daily_report_pdf, name='daily_report_pdf'),
    path('monthly/pdf/', views.monthly_report_pdf, name='monthly_report_pdf'),
    path('cash-reconciliation/pdf/', views.cash_reconciliation_pdf, name='cash_reconciliation_pdf'),
    path('audit-trail/pdf/', views.audit_trail_pdf, name='audit_trail_pdf'),
]