from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomerLoginForm, CustomerRegisterForm
from django.contrib.auth import login, authenticate
from .models import Customer

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request=request, message=f'Registered Successfully!')
            return redirect('CustomerRegister')    
        return render(request, 'BikeUsers/login.html', {'form': form})
    form = CustomerRegisterForm()
    return render(request, 'BikeUsers/register.html', {'form': form})


def customer_login(request):
    if request.method == "POST":
        form = CustomerLoginForm(request.POST)

        email = request.POST['email']
        password = request.POST['password']
        
        try:
            Customer.objects.get(email=email, password=password)
            messages.success(request=request, message=f'Logged in Successfully!')
            return redirect('CustomerHome')
                
        except Customer.DoesNotExist:
            messages.warning(request=request, message=f'Invalid email or password!')
            return render(request, 'BikeUsers/login.html', {'form': form})

    form = CustomerLoginForm()
    return render(request, 'BikeUsers/login.html', {'form': form})


def home(request):
    return render(request, 'BikeUsers/index.html')