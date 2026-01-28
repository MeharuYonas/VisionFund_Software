from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomerForm
from .models import Customer


# ----------------------------
# List all customers
# ----------------------------
@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-date_registered')
    return render(request, 'customers/customer_list.html', {
        'customers': customers
    })


# ----------------------------
# Customer detail
# ----------------------------
@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customers/customer_detail.html', {
        'customer': customer
    })


# ----------------------------
# Create customer
# ----------------------------
@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            customer = form.save(commit=False)
            customer.user = user
            customer.save()

            messages.success(request, 'Customer created successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'customers/customer_form.html', {
        'form': form
    })


# ----------------------------
# Update customer
# ----------------------------
@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            user = customer.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            customer = form.save(commit=False)
            customer.user = user
            customer.save()

            messages.success(request, 'Customer updated successfully!')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/customer_form.html', {
        'form': form
    })


# ----------------------------
# Delete customer
# ----------------------------
@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully!')
        return redirect('customer_list')

    return render(request, 'customers/customer_confirm_delete.html', {
        'customer': customer
    })
