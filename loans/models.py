from django.db import models
from customers.models import Customer
from datetime import date


# -----------------------------
# Main Loan model
# -----------------------------
class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('paid', 'Paid'),
        ('closed', 'Closed'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )  # principal
    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.0
    )  # annual %
    installments = models.PositiveIntegerField(
        default=1
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    applied_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-applied_date']
        verbose_name = "Loan"
        verbose_name_plural = "Loans"

    def __str__(self):
        return f"{self.customer.full_name} | {self.amount} | {self.status}"

    # Total payable amount (principal + interest)
    def total_payable(self):
        return self.amount + (self.amount * self.interest_rate / 100)

    # Amount per installment
    def installment_amount(self):
        if self.installments > 0:
            return round(self.total_payable() / self.installments, 2)
        return self.total_payable()


# -----------------------------
# Loan Repayment Schedule
# -----------------------------
class LoanRepayment(models.Model):
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name='repayments'
    )
    due_date = models.DateField()
    amount_due = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    amount_paid = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    paid_on = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['due_date']
        verbose_name = "Loan Repayment"
        verbose_name_plural = "Loan Repayments"

    def is_overdue(self):
        return self.amount_paid < self.amount_due and date.today() > self.due_date

    def __str__(self):
        return f"{self.loan.customer.full_name} | Due {self.amount_due} on {self.due_date}"


# -----------------------------
# Transaction Model
# -----------------------------
class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('loan_disbursement', 'Loan Disbursement'),
        ('loan_repayment', 'Loan Repayment'),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    loan = models.ForeignKey(
        Loan,
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,
        blank=True
    )
    transaction_type = models.CharField(
        max_length=30,
        choices=TRANSACTION_TYPE_CHOICES
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"{self.customer.full_name} | {self.transaction_type} | {self.amount}"
