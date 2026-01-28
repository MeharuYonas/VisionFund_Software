from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from django.utils.timezone import now
from datetime import date
import csv
import io
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required, user_passes_test

from savings.models import Saving
from loans.models import Loan, Transaction
from customers.models import Customer
from .models import AuditTrail
from .utils import export_csv, export_pdf

from django.template.loader import render_to_string
from weasyprint import HTML  # Optional: use ReportLab or WeasyPrint for nicer PDFs

# =========================
# ROLE CHECK FUNCTIONS
# =========================
def is_cashier(user):
    return user.groups.filter(name='Cashier').exists()

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def can_view_reports(user):
    return user.groups.filter(name__in=['Manager', 'Auditor', 'Cashier']).exists()

# =========================
# HTML REPORT VIEWS
# =========================

@login_required
@user_passes_test(can_view_reports)
def savings_report(request):
    savings = Saving.objects.select_related('customer').all()
    total_savings = savings.aggregate(total=Sum('balance'))['total'] or 0
    return render(request, 'reports/savings_report.html', {
        'savings': savings,
        'total_savings': total_savings,
    })

@login_required
@user_passes_test(can_view_reports)
def loan_portfolio(request):
    loans = Loan.objects.select_related('customer').all()
    totals = loans.aggregate(total_disbursed=Sum('amount'), outstanding=Sum('balance'))
    return render(request, 'reports/loan_portfolio.html', {
        'loans': loans,
        'total_disbursed': totals['total_disbursed'] or 0,
        'outstanding': totals['outstanding'] or 0,
    })

@login_required
@user_passes_test(is_manager)
def par_report(request):
    today = date.today()
    risky_loans = Loan.objects.filter(due_date__lt=today, balance__gt=0)
    total_portfolio = Loan.objects.count()
    par_count = risky_loans.count()
    par_ratio = (par_count / total_portfolio * 100) if total_portfolio else 0
    return render(request, 'reports/par_report.html', {
        'risky_loans': risky_loans,
        'par_ratio': round(par_ratio, 2),
        'par_count': par_count,
        'total_portfolio': total_portfolio,
    })

@login_required
@user_passes_test(can_view_reports)
def daily_report(request):
    today = date.today()
    report = Transaction.objects.filter(date=today).values('transaction_type').annotate(total=Sum('amount'))
    return render(request, 'reports/daily_report.html', {'report': report, 'date': today})

@login_required
@user_passes_test(can_view_reports)
def monthly_report(request):
    current_date = now()
    report = Transaction.objects.filter(
        date__month=current_date.month,
        date__year=current_date.year
    ).values('transaction_type').annotate(total=Sum('amount'))
    return render(request, 'reports/monthly_report.html', {'report': report, 'month': current_date.month, 'year': current_date.year})

@login_required
@user_passes_test(is_cashier)
def cash_reconciliation(request):
    today = date.today()
    inflow = Transaction.objects.filter(date=today, transaction_type__in=['SAVING', 'REPAYMENT']).aggregate(total=Sum('amount'))['total'] or 0
    outflow = Transaction.objects.filter(date=today, transaction_type__in=['LOAN', 'WITHDRAW']).aggregate(total=Sum('amount'))['total'] or 0
    opening_balance = 0
    expected_cash = opening_balance + inflow - outflow
    physical_cash = None
    difference = None
    if request.method == 'POST':
        physical_cash = float(request.POST.get('physical_cash', 0))
        difference = physical_cash - expected_cash
        AuditTrail.objects.create(user=request.user, action='CASH_RECONCILIATION', description=f'Cash reconciliation for {today}', amount=difference)
    return render(request, 'reports/cash_reconciliation.html', {
        'date': today,
        'opening_balance': opening_balance,
        'inflow': inflow,
        'outflow': outflow,
        'expected_cash': expected_cash,
        'physical_cash': physical_cash,
        'difference': difference,
    })

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Manager', 'Auditor']).exists())
def audit_trail_view(request):
    logs = AuditTrail.objects.all().order_by('-timestamp')[:100]
    return render(request, 'reports/audit_trail.html', {'logs': logs})

@login_required
@user_passes_test(can_view_reports)
def reports_dashboard(request):
    today = date.today()
    daily_summary = Transaction.objects.filter(date=today).values('transaction_type').annotate(total=Sum('amount'))
    monthly_summary = Transaction.objects.filter(date__month=today.month, date__year=today.year).values('transaction_type').annotate(total=Sum('amount'))
    inflow = Transaction.objects.filter(date=today, transaction_type__in=['SAVING', 'REPAYMENT']).aggregate(total=Sum('amount'))['total'] or 0
    outflow = Transaction.objects.filter(date=today, transaction_type__in=['LOAN', 'WITHDRAW']).aggregate(total=Sum('amount'))['total'] or 0
    expected_cash = inflow - outflow
    audit_logs = AuditTrail.objects.all().order_by('-timestamp')[:10]
    return render(request, 'reports/reports_dashboard.html', {
        'today': today,
        'daily_summary': daily_summary,
        'monthly_summary': monthly_summary,
        'expected_cash': expected_cash,
        'audit_logs': audit_logs,
    })

# =========================
# CSV EXPORT FUNCTIONS
# =========================

@login_required
@user_passes_test(can_view_reports)
def export_savings_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="savings_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Customer', 'Saving Type', 'Amount', 'Withdraw', 'Balance', 'Date'])
    savings = Saving.objects.select_related('customer').all()
    for s in savings:
        writer.writerow([s.customer.full_name, s.saving_type, s.amount, s.withdraw, s.balance, s.date.strftime('%Y-%m-%d')])
    return response

@login_required
@user_passes_test(can_view_reports)
def export_loans_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="loans_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Customer', 'Amount', 'Status', 'Applied Date'])
    for loan in Loan.objects.all():
        writer.writerow([loan.customer.full_name, loan.amount, loan.status, loan.applied_date])
    return response

@login_required
@user_passes_test(can_view_reports)
def export_transactions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Customer', 'Transaction Type', 'Amount', 'Date'])
    for t in Transaction.objects.select_related('customer').all():
        writer.writerow([t.customer.full_name, t.transaction_type, t.amount, t.date.strftime('%Y-%m-%d %H:%M')])
    return response

@login_required
@user_passes_test(can_view_reports)
def cash_reconciliation_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cash_reconciliation.csv"'
    writer = csv.writer(response)
    writer.writerow(['Customer', 'Transaction Type', 'Amount', 'Date'])
    transactions = Transaction.objects.select_related('customer').all()
    for t in transactions:
        writer.writerow([t.customer.full_name, t.transaction_type, t.amount, t.date.strftime('%Y-%m-%d %H:%M')])
    return response

@login_required
@user_passes_test(can_view_reports)
def audit_trail_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="audit_trail.csv"'
    writer = csv.writer(response)
    writer.writerow(['User', 'Action', 'Description', 'Amount', 'Timestamp'])
    logs = AuditTrail.objects.all().order_by('-timestamp')
    for log in logs:
        writer.writerow([log.user.username if log.user else '', log.action, log.description, log.amount, log.timestamp.strftime('%Y-%m-%d %H:%M')])
    return response

# =========================
# PDF EXPORT FUNCTIONS
# =========================

def generate_pdf_response(title):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, title)
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

@login_required
@user_passes_test(can_view_reports)
def export_savings_pdf(request):
    return generate_pdf_response("Savings Report PDF")

@login_required
@user_passes_test(can_view_reports)
def export_loans_pdf(request):
    return generate_pdf_response("Loans Report PDF")

@login_required
@user_passes_test(can_view_reports)
def export_transactions_pdf(request):
    return generate_pdf_response("Transactions Report PDF")

@login_required
@user_passes_test(can_view_reports)
def cash_reconciliation_pdf(request):
    return generate_pdf_response("Cash Reconciliation PDF")

@login_required
@user_passes_test(can_view_reports)
def audit_trail_pdf(request):
    return generate_pdf_response("Audit Trail PDF")

# Role check
def can_view_reports(user):
    return user.groups.filter(name__in=['Manager', 'Auditor', 'Cashier']).exists()


# -------------------
# DAILY REPORT CSV
# -------------------
@login_required
@user_passes_test(can_view_reports)
def daily_report_csv(request):
    today = date.today()
    transactions = Transaction.objects.filter(date=today)
    fields = ['transaction_type', 'amount', 'created_by', 'date']
    return export_csv(transactions, fields, f'daily_report_{today}.csv')


# -------------------
# MONTHLY REPORT CSV
# -------------------
@login_required
@user_passes_test(can_view_reports)
def monthly_report_csv(request):
    today = date.today()
    transactions = Transaction.objects.filter(
        date__month=today.month,
        date__year=today.year
    )
    fields = ['transaction_type', 'amount', 'created_by', 'date']
    return export_csv(transactions, fields, f'monthly_report_{today.month}_{today.year}.csv')


# Role check
def can_view_reports(user):
    return user.groups.filter(name__in=['Manager', 'Auditor', 'Cashier']).exists()


# -------------------
# DAILY REPORT PDF
# -------------------
@login_required
@user_passes_test(can_view_reports)
def daily_report_pdf(request):
    today = date.today()
    report = Transaction.objects.filter(date=today).values('transaction_type').annotate(total_amount=Sum('amount'))
    
    context = {
        'report': report,
        'date': today
    }
    return export_pdf('reports/daily_report_pdf.html', context, f'daily_report_{today}.pdf')


# -------------------
# MONTHLY REPORT PDF
# -------------------
@login_required
@user_passes_test(can_view_reports)
def monthly_report_pdf(request):
    today = date.today()
    report = Transaction.objects.filter(
        date__month=today.month,
        date__year=today.year
    ).values('transaction_type').annotate(total_amount=Sum('amount'))

    context = {
        'report': report,
        'month': today.month,
        'year': today.year
    }
    return export_pdf('reports/monthly_report_pdf.html', context, f'monthly_report_{today.month}_{today.year}.pdf')


# -------------------
# CASH RECONCILIATION PDF
# -------------------
@login_required
@user_passes_test(can_view_reports)
def cash_reconciliation_pdf(request):
    today = date.today()
    transactions = Transaction.objects.filter(date=today)
    context = {
        'transactions': transactions,
        'date': today
    }
    return export_pdf('reports/cash_reconciliation_pdf.html', context, f'cash_reconciliation_{today}.pdf')


# -------------------
# AUDIT TRAIL PDF
# -------------------
@login_required
@user_passes_test(can_view_reports)
def audit_trail_pdf(request):
    from .models import AuditTrail
    logs = AuditTrail.objects.all().order_by('-timestamp')[:100]
    context = {
        'logs': logs
    }
    return export_pdf('reports/audit_trail_pdf.html', context, 'audit_trail.pdf')
