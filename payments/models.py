from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Wallet
from django.db.models.signals import post_save
from django.dispatch import receiver

# Get the User model
User = get_user_model()

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Maya', 'Maya'),
        ('GCash', 'GCash'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        default='Maya'
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.reference_number} - {self.status} ({self.payment_method})"

class Withdrawal(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('gcash', 'GCash'),
        ('paymaya', 'PayMaya'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending',
    )

    def __str__(self):
        return f"{self.user.username} - ₱{self.amount} ({self.status})"

    def approve(self):
        if self.status == 'pending' and self.amount <= self.user.wallet.balance:
            self.status = 'approved'
            self.user.wallet.balance -= self.amount
            self.user.wallet.save()
            self.save()


