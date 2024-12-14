from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Wallet

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # Perform authentication logic here
        if authenticate(username=username, password=password):  # Replace with your auth logic
            messages.success(request, 'Login successful!')
            return redirect('/Game/dashboard/')  # Replace 'home' with your redirect URL
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('/accounts/login/')  # Redirect back to login page
    return render(request, 'login.html')
