
# Create your views here.
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Sum
from accounts.models import CustomUser
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db import models
from accounts.models import Wallet
from django.http import JsonResponse
from django.utils.timezone import now
from django.shortcuts import render
import random




@login_required
def dashboard(request):
    try:
        # Try to access the wallet for the logged-in user
        wallet = request.user.wallet
    except Wallet.DoesNotExist:
        # Handle case where user doesn't have a wallet, wallet remains None
        pass  # No need to assign anything as it's already set to None
    
    # If wallet is None, create a new wallet for the user
    if wallet is None:
        wallet = Wallet.objects.create(user=request.user)
    
    return render(request, 'dashboard.html', {'wallet': wallet})


def flappy_game(request):
    return render(request, 'flappy.html')


def game_icons(request):
    return render(request, 'game.html')

def referal(request):
    return render(request, 'referal.html')

def scatter(request):
    return render (request, 'scatter.html')




