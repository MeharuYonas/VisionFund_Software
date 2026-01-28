from django.db import models
from customers.models import Customer


class Saving(models.Model):
    SAVING_TYPE_CHOICES = [
        ('compulsory', 'Compulsory'),
        ('voluntary', 'Voluntary'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='savings'
    )
    saving_type = models.CharField(
        max_length=20,
        choices=SAVING_TYPE_CHOICES
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    withdraw = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Saving"
        verbose_name_plural = "Savings"

    def __str__(self):
        return f"{self.customer.full_name} | {self.saving_type} | {self.balance}"

def save(self, *args, **kwargs):
    self.balance = self.amount - self.withdraw
    super().save(*args, **kwargs)

def save(self, *args, **kwargs):
    self.balance = self.amount - self.withdraw
    super().save(*args, **kwargs)
