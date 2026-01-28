from django.db import models
from django.contrib.auth.models import User

class AuditTrail(models.Model):
    ACTION_CHOICES = [
        ('CASH_ENTRY', 'Cash Entry'),
        ('CASH_RECONCILE', 'Cash Reconciliation'),
        ('LOAN_DISBURSE', 'Loan Disbursement'),
        ('LOAN_REPAY', 'Loan Repayment'),
        ('SAVINGS', 'Savings Transaction'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"

class Saving(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.date}"
