from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def register(request):
    return render(request, 'register.html')

def rewards(request):
    return render(request, 'rewards.html')

def customer_service(request):
    return render(request, 'service.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash the password
            user.save()  # Save the user to the database
            messages.success(request, "Registration successful!")
            return redirect('/')  # Redirect to the login page
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})



def home_game(request):
    return render(request, 'home-game.html')