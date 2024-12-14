from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import PaymentForm
from accounts.models import Wallet
from django.db import transaction
from .models import Withdrawal
from django.contrib import messages
from accounts.models import Wallet


@login_required
def payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():  # Ensure atomicity
                payment = form.save(commit=False)  # Do not save yet
                payment.user = request.user       # Assign the logged-in user
                payment.status = 'Pending'       # Mark the payment as pending
                payment.save()                   # Save the payment request

                # Ensure the wallet exists for the user
                Wallet.objects.get_or_create(user=request.user)

            # Redirect back to the dashboard or another confirmation page
            return redirect('/Game/dashboard/')  # Redirect to the dashboard view
    else:
        form = PaymentForm()

    return render(request, "methods.html", {"form": form})

@login_required
def withdraw(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        payment_method = request.POST.get("payment_method")
        phone_number = request.POST.get("phone_number")

        if request.user.wallet.balance >= float(amount):
            # Create a new withdrawal request
            withdrawal = Withdrawal.objects.create(
                user=request.user,
                amount=amount,
                payment_method=payment_method,
                phone_number=phone_number,
            )
            withdrawal.save()
            messages.success(request, "Withdrawal request submitted!")
        else:
            messages.error(request, "Insufficient balance!")
        return redirect("/Game/dashboard/")

    return render(request, "withdraw.html")
