from django.shortcuts import render, redirect
from .models import Saving
from .forms import SavingForm

# List of savings
def saving_list(request):
    savings = Saving.objects.all()
    return render(request, 'savings/saving_list.html', {'savings': savings})

# Deposit / Create Saving
def saving_create(request):
    if request.method == 'POST':
        form = SavingForm(request.POST)
        if form.is_valid():
            saving = form.save(commit=False)
            # Update balance: add current amount to previous balance of same customer
            last_saving = Saving.objects.filter(customer=saving.customer).order_by('-date').first()
            if last_saving:
                saving.balance = last_saving.balance + saving.amount
            else:
                saving.balance = saving.amount
            saving.save()
            return redirect('saving_list')
    else:
        form = SavingForm()
    return render(request, 'savings/saving_form.html', {'form': form})

# Withdrawal
def saving_withdraw(request, pk):
    saving = Saving.objects.get(pk=pk)
    if request.method == 'POST':
        withdraw_amount = float(request.POST['amount'])
        if withdraw_amount <= saving.balance:
            saving.balance -= withdraw_amount
            saving.save()
        return redirect('saving_list')
    return render(request, 'savings/withdraw_form.html', {'saving': saving})

