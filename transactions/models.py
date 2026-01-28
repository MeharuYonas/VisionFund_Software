from django.db import models
from loans.models import Loan
from savings.models import Saving

class Transaction(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    transaction_type = models.CharField(max_length=20, choices=[('deposit','Deposit'),('withdraw','Withdraw'),('repayment','Repayment')])

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
