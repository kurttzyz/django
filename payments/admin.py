from django.contrib import admin
from .models import Payment
from decimal import Decimal  # Import Decimal
from django.contrib.auth.models import User  # or your custom User model
from accounts.models import Wallet
from django.contrib import admin
from .models import Withdrawal

# Custom action to verify payments and update user wallets
@admin.action(description="Verify payments")
def verify_payments(modeladmin, request, queryset):
    for payment in queryset:
        if payment.status == 'Pending':
            print(f"Verifying payment with reference number: {payment.reference_number}")
            
            # Update payment status
            payment.status = 'Verified'
            payment.save()
            
            user = payment.user
            wallet, created = Wallet.objects.get_or_create(user=user)

            print(f"Old balance: {wallet.balance}")
            wallet.balance += payment.amount
            wallet.save()

            print(f"New balance: {wallet.balance}")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # Include 'user' in the list display to show it in the admin panel
    list_display = ('user', 'reference_number', 'amount', 'payment_method', 'status', 'date_created')
    list_filter = ('status', 'payment_method', 'date_created', 'user')  # Add user to the filter options
    search_fields = ('reference_number', 'payment_method', 'user__username')  # Enable search by user username
    ordering = ('-date_created',)

    # Include 'user' in the form fields and readonly fields as needed
    fields = ('user', 'amount', 'reference_number', 'status', 'payment_method', 'date_created')
    readonly_fields = ('date_created',)

    # Define available actions
    actions = [verify_payments]  # Add your custom actions here



@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_method', 'phone_number', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username',)
    actions = ['approve_withdrawals', 'reject_withdrawals']

    def approve_withdrawals(self, request, queryset):
        for withdrawal in queryset.filter(status='pending'):
            if withdrawal.amount <= withdrawal.user.wallet.balance:
                withdrawal.status = 'approved'
                withdrawal.user.wallet.balance -= withdrawal.amount
                withdrawal.user.wallet.save()
                withdrawal.save()
        self.message_user(request, "Selected withdrawals have been approved.")

    approve_withdrawals.short_description = "Approve selected withdrawals"

    def reject_withdrawals(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f"{updated} withdrawal(s) marked as Rejected.")

    reject_withdrawals.short_description = "Reject selected withdrawals"