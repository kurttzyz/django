from django.db import models
from django.contrib.auth.models import User
from django.db import models
from accounts.models import CustomUser
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User


class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)  # this should be start_time if you renamed it to start_time
    end_time = models.DateTimeField(null=True, blank=True)
    amount_wagered = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_won = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"GameSession {self.id} for {self.user.username} with score {self.score}"


class Game(models.Model):
    name = models.CharField(max_length=100, default="Flappy Bird")
    created_at = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('bet', 'Bet'),
        ('win', 'Win'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    balance_after_transaction = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Verified', 'Verified'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.reference_number} - {self.status}"
   


