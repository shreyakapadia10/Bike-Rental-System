from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages.api import success
from django.shortcuts import redirect, render
from .forms import CustomerCreationForm, CustomerLoginForm,BikeRegistrationForm
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_view
from django.views.generic import ListView, DetailView
from .models import bike

# Create your views here.
# def register(request):
#     if request.method == 'POST':
#         form = CustomerRegisterForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             form.save()
#             messages.success(request=request, message=f'Registered Successfully!')
#             return redirect('CustomerRegister')    
#         return render(request, 'BikeUsers/login.html', {'form': form})
#     form = CustomerRegisterForm()
#     return render(request, 'BikeUsers/register.html', {'form': form})


# def SignIn(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request=request.POST)

#         username = request.POST['username']
#         password = request.POST['password']
        
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('CustomerHome')
#         else:
#            messages.warning(request=request, message='Please check your credentials again!')
#     form = AuthenticationForm()
#     return render(request=request, template_name='BikeUsers/login.html', context={'form': form})

def home(request):
    if request.user.is_authenticated:
        return render(request, 'BikeUsers/index.html')
    else:
        return redirect('CustomerLogin')


class SignUpView(CreateView):
    form_class = CustomerCreationForm
    success_url = reverse_lazy('CustomerLogin')
    template_name = 'BikeUsers/register.html'
    success_message = 'Registered Successfully! You can now login with your username!'


class SignIn(auth_view.LoginView):
    form_class = CustomerLoginForm
    success_url = reverse_lazy('CustomerHome')
    template_name = 'BikeUsers/login.html'
    success_message = 'Logged in successfully!'
    redirect_authenticated_user = True

class BikeAddView(CreateView):
    form_class = BikeRegistrationForm
    success_url = reverse_lazy('CustomerLogin')
    template_name = 'BikeUsers/bikeadd.html'

class Bikedetails(DetailView):
    model = bike
    template_name = 'BikeUsers/BikeDetails.html'  