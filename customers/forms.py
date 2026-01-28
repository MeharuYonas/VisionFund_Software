from django import forms
from django.forms.widgets import DateInput
from django.contrib.auth.models import User
from .models import Customer

class CustomerForm(forms.ModelForm):
    # Fields from the related User model
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Customer
        fields = [
            'national_id',
            'full_name',
            'sex',
            'date_of_birth',
            'department',
            'phone',
            'address',
            'responsibility',
            'first_name',
            'last_name',
            'email',
        ]
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Address'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'National ID'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'responsibility': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Responsibility'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing an existing customer, populate User fields
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        # Save the Customer model first, without committing
        customer = super().save(commit=False)

        # Save the User model fields
        user = customer.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()      # Save User first
            customer.save()  # Then save Customer
        return customer
