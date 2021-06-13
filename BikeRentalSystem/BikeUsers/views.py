from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.api import success
from django.shortcuts import redirect, render
from .forms import CustomerCreationForm, CustomerLoginForm,BikeRegistrationForm, BikeUpdateForm
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView,  UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_view
from .models import bike, Rating, Customer
from django.http import JsonResponse
from django.http import HttpResponse

import smtplib
import random
import email.message

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


class BikeAddView(LoginRequiredMixin, CreateView):
    form_class = BikeRegistrationForm
    success_url = reverse_lazy('CustomerLogin')
    template_name = 'BikeUsers/bikeadd.html'
    def form_valid(self, form):
        form.instance.operatorid = self.request.user
        return super().form_valid(form)


class BikeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model=bike
    form_class = BikeUpdateForm
    success_url = reverse_lazy('CustomerLogin')
    template_name = 'BikeUsers/bikeadd.html'
    def form_valid(self, form):
        form.instance.operatorid = self.request.user
        return super().form_valid(form)
    def test_func(self):
        bike= self.get_object()

        if bike.operatorid== self.request.user:
            return True
        return False


class BikeDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model=bike
    success_url = reverse_lazy('CustomerLogin')
    template_name = 'BikeUsers/bike_detail_confirm_delete.html'
    success_message = "Bike Details Deleted Successfully!"
    def delete(self, request, *args, **kwargs):
        messages.success(request=request, message=self.success_message)
        return super().delete(request, *args, **kwargs)
    def test_func(self):
        bike= self.get_object()

        if bike.operatorid== self.request.user:
            return True
        return False

class Rettingadd(LoginRequiredMixin, CreateView):
    model=Rating
    fields = '__all__'
    success_url = reverse_lazy('CustomerLogin')
    template_name = 'BikeUsers/feedback.html'
    success_message = 'Thank you for your valueable response!'

#def feedback1(request):
 #   if request.method=='POST' and star!=null:
  #      star=request.POST['star']
   #     suggestions=request.POST['suggestions']
    #    Rating=Rating.objects.create(star=full_name,suggestions=suggestions,message=message)
     #   messages.success(request,'Thank you for your valueable response!')
   # return render(request,'contact.html')

def CompForgetPass(request):
    if request.POST:
        em1 = request.POST['em']
        try:
            valid = Company_Details.objects.get(c_email = em1)
            print(valid)
            
            sender_email = "rinkal.bisagn.internship@gmail.com"
            sender_pass = 'bisagn@106'
            reciv_email = em1      
            
            server = smtplib.SMTP('smtp.gmail.com',587)
            
            # OTP Create---------
            nos = [1,2,3,4,5,6,7,8,9,0]
            otp = ""
            for i in range(6):
                otp += str(random.choice(nos))
                print(otp)
            print(otp)
            
            mes1 = f"""
            This Is Your OTP From This New Site
            {otp}
            
            
            Note:- Don't share With Others......
            """
            
            msg = email.message.Message()
            msg['Subject'] = "OTP From This Site"
            msg['From'] = sender_email
            msg['To'] = reciv_email
            password = sender_pass
            msg.add_header('Content-Type','text/html')
            msg.set_payload(mes1)
            
            server.starttls()
            server.login(msg['From'],password)
            server.sendmail(msg['From'],msg['To'],msg.as_string())
            
            request.session['otp'] = otp
            request.session['New_User'] = valid.id  
            
            print(request.session['New_User'])
            print(request.session['otp'])
            return redirect('OTP_checker')
        except:
            return HttpResponse("<a href=''> You Have Entered Wrong Email Id </a>")
    return render(request,'company/login/ForgetPass.html')

def OTP_checker(request):
    if 'otp' in request.session.keys():
        if request.POST:
            ot1 = request.POST['otp'] 
            print(ot1)
            print(request.session['otp'])
            if request.session['otp'] == ot1:
                del request.session['otp']
                return redirect('Create_NewPass')
            else:
                del request.session['otp']
                return redirect('CompForgetPass')
        return render(request,'company/login/otp_check.html')
    else:
        return redirect('c_login')


def Create_NewPass(request):
    if 'New_User' in request.session.keys():
        if request.POST:
            p1 = request.POST['pass1']
            p2 = request.POST['pass2']
            print(p1,p2)
            if p1 == p2:
                obj = Company_Details.objects.get(id=int(request.session['New_User']))
                obj.c_pass = p2
                obj.save()
                del request.session['New_User']
                return redirect('c_login')
            else:
                return HttpResponse('<a href=""> Both Passwords Are not Same </a>')
        return render(request,'company/login/New_Pass1.html')
    else:
        return redirect('CompForgetPass')



