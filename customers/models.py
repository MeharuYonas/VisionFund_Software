from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='customer_profile'
    )
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    department = models.CharField(max_length=50, blank=True, null=True)
    responsibility = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        if self.user:
            return self.user.username
        return self.full_name
    
user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)