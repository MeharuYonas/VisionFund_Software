from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test  # ✅ ADD THIS
from .models import Loan, LoanRepayment
from .forms import LoanForm
from datetime import date, timedelta

# Loan list
def loan_list(request):
    loans = Loan.objects.all()
    return render(request, 'loans/loan_list.html', {'loans': loans})

# Apply / Create Loan
def loan_apply(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.status = 'pending'
            loan.save()
            return redirect('loan_list')
    else:
        form = LoanForm()
    return render(request, 'loans/loan_form.html', {'form': form})

# Approve / Reject Loan
def loan_approve(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            loan.status = 'approved'
            loan.approved_date = timezone.now()
            loan.due_date = timezone.now() + timezone.timedelta(days=30)  # example 1 month loan
        elif action == 'reject':
            loan.status = 'rejected'
        loan.save()
        return redirect('loan_list')
    return render(request, 'loans/loan_approve.html', {'loan': loan})

from django.shortcuts import render
from datetime import timedelta

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Manager','Auditor','Cashier']).exists())
def loan_repayment_schedule(request):
    loans = Loan.objects.filter(status='Active')
    schedules = []

    for loan in loans:
        # Check if repayment schedule exists
        repayments = LoanRepayment.objects.filter(loan=loan).order_by('due_date')
        if not repayments.exists():
            # Generate schedule
            monthly_amount = loan.monthly_repayment()
            for i in range(loan.term_months):
                due_date = loan.start_date + timedelta(days=30*i)
                LoanRepayment.objects.create(
                    loan=loan,
                    due_date=due_date,
                    amount_due=monthly_amount
                )
            repayments = LoanRepayment.objects.filter(loan=loan).order_by('due_date')

        schedules.append({'loan': loan, 'repayments': repayments})

    return render(request, 'loans/loan_repayment_schedule.html', {'schedules': schedules})

from django.http import HttpResponse
import csv

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Manager','Auditor','Cashier']).exists())
def loan_repayment_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="loan_repayment_schedule.csv"'
    writer = csv.writer(response)
    writer.writerow(['Borrower','Loan ID','Due Date','Amount Due','Amount Paid','Status'])

    loans = Loan.objects.filter(status='Active')
    for loan in loans:
        for repayment in LoanRepayment.objects.filter(loan=loan).order_by('due_date'):
            status = 'Overdue' if repayment.is_overdue() else 'Paid' if repayment.amount_paid >= repayment.amount_due else 'Pending'
            writer.writerow([loan.borrower.username, loan.id, repayment.due_date, repayment.amount_due, repayment.amount_paid, status])

    return response

from reports.utils import export_pdf

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Manager','Auditor','Cashier']).exists())
def loan_repayment_pdf(request):
    loans = Loan.objects.filter(status='Active')
    schedules = []
    for loan in loans:
        repayments = LoanRepayment.objects.filter(loan=loan).order_by('due_date')
        schedules.append({'loan': loan, 'repayments': repayments})
    context = {'schedules': schedules}
    return export_pdf('loans/loan_repayment_pdf.html', context, filename='loan_repayment_schedule.pdf')

from datetime import timedelta, date

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Manager','Auditor','Cashier']).exists())
def loan_repayment_mortgage(request):
    loans = Loan.objects.filter(status='Active')
    schedules = []

    for loan in loans:
        repayments = LoanRepayment.objects.filter(loan=loan).order_by('due_date')
        if not repayments.exists():
            # Generate mortgage repayment schedule
            balance = float(loan.principal)
            monthly_payment = loan.mortgage_monthly_payment()
            monthly_rate = float(loan.interest_rate)/100/12

            for i in range(loan.term_months):
                interest = round(balance * monthly_rate, 2)
                principal_paid = round(monthly_payment - interest, 2)
                balance = round(balance - principal_paid, 2)
                due_date = loan.start_date + timedelta(days=30*i)

                LoanRepayment.objects.create(
                    loan=loan,
                    due_date=due_date,
                    amount_due=monthly_payment,
                    amount_paid=0
                )

        repayments = LoanRepayment.objects.filter(loan=loan).order_by('due_date')
        schedules.append({'loan': loan, 'repayments': repayments})

    return render(request, 'loans/loan_repayment_mortgage.html', {'schedules': schedules})


def loan_repayment_mortgage(request):
    return render(request, 'loans/repayment_mortgage.html')


def loan_repayment_mortgage_csv(request):
    ...
