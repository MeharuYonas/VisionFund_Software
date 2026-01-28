from django import forms
from .models import Loan

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['customer', 'amount', 'interest_rate', 'installments']
