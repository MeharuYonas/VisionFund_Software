from django import forms
from .models import Income, Expense

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount']

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder':'Username', 'class':'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Password', 'class':'form-control'
    }))
