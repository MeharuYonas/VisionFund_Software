from django import forms
from django.forms.widgets import DateInput
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth import get_user_model

User = get_user_model()

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

class CustomerForm(forms.ModelForm):

    def save(self, commit=True):
        customer = super().save(commit=False)

        # CREATE USER if not exists
        user = getattr(customer, "user", None)

        if user is None:
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=User.objects.make_random_password()
            )

        # UPDATE USER FIELDS
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()

        # LINK USER TO CUSTOMER
        customer.user = user

        if commit:
            customer.save()

        return customer
