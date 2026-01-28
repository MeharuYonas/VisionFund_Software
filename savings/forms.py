from django import forms
from .models import Saving

class SavingForm(forms.ModelForm):
    class Meta:
        model = Saving
        fields = ['customer', 'saving_type', 'amount']
