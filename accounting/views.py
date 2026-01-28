from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Income, Expense, CashOnHand
from .forms import IncomeForm, ExpenseForm
from django.utils import timezone

def daily_cash_summary(request):
    today = timezone.now().date()

    income_total = Income.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = Expense.objects.filter(date=today).aggregate(Sum('amount'))['amount__sum'] or 0

    last_cash = CashOnHand.objects.last()
    opening_balance = last_cash.closing_balance if last_cash else 0

    closing_balance = opening_balance + income_total - expense_total

    CashOnHand.objects.update_or_create(
        date=today,
        defaults={
            'opening_balance': opening_balance,
            'closing_balance': closing_balance
        }
    )

    return render(request, 'accounting/daily_summary.html', {
        'opening': opening_balance,
        'income': income_total,
        'expense': expense_total,
        'closing': closing_balance
    })

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm

def login_view(request):
    if request.user.is_authenticated:
        # Redirect based on role
        if request.user.groups.filter(name='Manager').exists():
            return redirect('reports_dashboard')
        elif request.user.groups.filter(name='Cashier').exists():
            return redirect('reports_dashboard')
        elif request.user.groups.filter(name='Auditor').exists():
            return redirect('reports_dashboard')
        else:
            return redirect('customer_list')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                # Redirect based on role
                if user.groups.filter(name='Manager').exists():
                    return redirect('reports_dashboard')
                elif user.groups.filter(name='Cashier').exists():
                    return redirect('reports_dashboard')
                elif user.groups.filter(name='Auditor').exists():
                    return redirect('reports_dashboard')
                else:
                    return redirect('customer_list')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request,"You have been logged out.")
    return redirect('login')

from django.shortcuts import render

def login_view(request):
    return render(request, 'accounting/login.html')
