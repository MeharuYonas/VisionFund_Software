from django.db import models
from django.utils import timezone

class CashOnHand(models.Model):
    date = models.DateField(default=timezone.now)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.closing_balance}"

class Income(models.Model):
    date = models.DateField(default=timezone.now)
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.source} - {self.amount}"

class Expense(models.Model):
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.description} - {self.amount}"
