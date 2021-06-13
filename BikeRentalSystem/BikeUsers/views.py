from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.api import success
from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView,  UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_view
from .models import *
from django.http import JsonResponse, HttpResponse
import smtplib
import random
import email.message
from django.core.serializers import serialize
import json
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required


def home(request):
	if request.user.is_authenticated:
		stations = Station.objects.all()
		if len(stations) > 0:
			station_json = serialize('json', stations)
			form = CityForm()
			return render(request, 'BikeUsers/index.html', {'stations': station_json, 'form': form})
		else:
			form = CityForm()
			return render(request, 'BikeUsers/index.html', {'stations': '', 'form': form})

	else:
		return redirect('CustomerLogin')


def search_station(request):
	if request.is_ajax():
		is_pincode = request.POST.get('is_pincode', None)
		is_city = request.POST.get('is_city', None)
		stations = ""

		# If user has searched via pincode
		if is_pincode == 'true':
			# getting data from pincodeText input
			pincode = request.POST.get('pincodeText', None)

			if pincode:  # cheking if pincodeText has value
				stations = Station.objects.filter(post_code=int(pincode))

		# If user has searched via city
		if is_city == 'true':
			city = request.POST.get('city', None)

			if city:
				stations = Station.objects.filter(city=city)

		# Sending list of stations to user

		# If stations found with given pincode or city
		if len(stations) > 0:
			station_json = serialize('json', stations)
			response = {
				'stations': station_json
			}

		# If no station found with given pincode or city, send blank data
		else:
			response = {
				'stations': ''
			}
		return JsonResponse(response)  # return response as JSON

	# If user has come here via any other request except ajax, redirect to home page again
	else:
		return redirect('CustomerHome')


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



    

class MapsView(CreateView):
    form_class = MapsForm
    template_name = 'BikeUsers/index.html'
    success_url = reverse_lazy('CustomerHome')
def search_city(request):
	if request.is_ajax():
		# getting data from state input
		state = request.POST.get('state', None)

		if state:  # cheking if state has value
			
			cities = City.objects.filter(state=state)

			city_json = serialize('json', cities)
			response = {
				'cities': city_json
			}
			
			return JsonResponse(response)  # return response as JSON
	else:
		return redirect('CustomerHome')


def get_map(request, pk):
	station = Station.objects.get(id=pk)
	station_json = serialize('json',[station])
	return render(request=request, template_name='BikeUsers/get_map.html', context={'station': station_json})

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


class AddStationView(CreateView):
	form_class = MapsForm
	template_name = 'BikeUsers/add_station.html'
	success_url = reverse_lazy('AddStation')


def add_station(request):
	up_form = MapsForm()
	result = "error"
	message = "Something went wrong. Please check and try again"

	if request.is_ajax() and request.method == "POST":
		up_form = MapsForm(data = request.POST)
		
		#if both forms are valid, do something
		if up_form.is_valid():
			up_form.save()

			result = "perfect"
			message = "Station Details Added Successfully!"
			context = {"result": result, "message": message,}
		else:
			message = "Station Details Can't Be Added, Try again!"
			context = {"result": result, "message": message}

		return HttpResponse(
			json.dumps(context),
			content_type="application/json"
			)
		
	context = {
		'up_form':up_form,
		}
	return render(request, 'BikeUsers/add_station.html', context)

def bikeinfo(request):
	bikes=bike.objects.all()
	paginate_by = 2
	return render(request, 'BikeUsers/viewbike.html', {'viewbike': bikes })

@login_required
def CustomerUpdateView(request):
    if request.method == 'POST':
        u_form = CustomerUpdateForm(request.POST,instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request,'Your Profile has been updated!')
            return redirect('CustomerHome')
        else:
             messages.error(request,'Please Enter Correct')
    else:
        u_form = CustomerUpdateForm(instance=request.user)

    context={ 'u_form': u_form}
    return render(request, 'BikeUsers/update_customer.html',context )


class Bikedetails(DetailView):
    model = bike
    template_name = 'BikeUsers/BikeDetails.html'  
