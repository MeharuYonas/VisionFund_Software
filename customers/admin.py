from django.contrib import admin
from django.contrib.auth.models import User
from .models import Customer
from .forms import CustomerForm

# Unregister the Customer model if it was previously registered
# This prevents AlreadyRegistered errors
try:
    admin.site.unregister(Customer)
except admin.sites.NotRegistered:
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm  # Use the custom form
    list_display = ('user', 'full_name', 'phone', 'department', 'responsibility')
    search_fields = ('user__username', 'user__email', 'phone', 'full_name')
    list_filter = ('department', 'sex')
    ordering = ('full_name',)

    # Optional: Customize how User fields appear in admin form
    fieldsets = (
        ('User Information', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Customer Details', {
            'fields': ('national_id', 'full_name', 'sex', 'date_of_birth', 
                       'department', 'phone', 'address', 'responsibility')
        }),
    )
