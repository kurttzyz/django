from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    
    # Adding related_name to prevent clashes with the default User model
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='customuser_set',  # Custom related_name
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permission_set',  # Custom related_name
        blank=True
    )

class Wallet(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Dynamically reference the User modelx
        on_delete=models.CASCADE,
        related_name="wallet"
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


