from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Wallet

# Customizing the User Admin to include custom fields
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Fields to display in the admin panel for the user
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('wallet',)}),  # Add the wallet field
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('wallet',)}),  # Add wallet field when adding new user
    )

# Register CustomUser with the CustomUserAdmi

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')  # Display user and balance fields in the list view
    search_fields = ('user__username',)  # Allow searching by username
    list_filter = ('user',)  # Filter wallets by user


admin.site.register(Wallet, WalletAdmin)

