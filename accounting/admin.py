from django.contrib import admin
from .models import CashOnHand, Income, Expense

admin.site.register(CashOnHand)
admin.site.register(Income)
admin.site.register(Expense)
