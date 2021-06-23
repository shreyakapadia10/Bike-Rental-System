from datetime import date
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_view
from django.http import JsonResponse, HttpResponse, response
from django.views.generic import DetailView
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
import smtplib
import random
import email.message
import json
from .models import *
from .forms import *
from datetime import datetime

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


def bikeinfo(request, pk):
    bikes=bike.objects.filter(station_id=pk)
    paginate_by = 2
    return render(request, 'BikeUsers/viewbike.html', {'viewbike': bikes, 'station': pk })


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
    return render(request, 'BikeUsers/update_customer.html',context)


class Bikedetails(DetailView):
    model = bike
    template_name = 'BikeUsers/BikeDetails.html'


def check_bikes(request):
    if request.is_ajax():
        # Getting form data
        from_date = request.POST.get('from_date', None)
        to_date = request.POST.get('to_date', None)
        from_time = request.POST.get('from_time', None)
        to_time = request.POST.get('to_time', None)
        station_id = request.POST.get('station_id', None)

        # Calling user defined format_date function to format the date and time
        from_date, to_date, from_date_time, to_date_time = format_date(from_date, to_date, from_time, to_time)

        # Calculatig duration
        duration = to_date_time - from_date_time
        duration_in_s  = duration.total_seconds()

        # Getting number of days and hours
        days = divmod(duration_in_s, 86400) # Get days (without [0]!)
        hours = divmod(days[1], 3600) # Use remainder of days to calc hours

        # Getting bikes which are on rent on given date and time of particular station
        # To select between range the field name is combined with '__range' and start and end date is provided

        bike_rent_history = BikeRentHistory.objects.filter(from_date_time__range=(from_date, to_date), station=station_id)

        bikes_available = ""

        # if queryset is not empty
        if len(bike_rent_history) > 0:
            # Looping over query set 'bike_rent_history'
            for field in bike_rent_history:
                
                # Excluding those bikes which are on rent on selected date and time
                bikes_available = bike.objects.exclude(id=field.bike_id)
                # print(bikes_available)

        # If no such bikes find between given date and time range
        else:
            bikes_available = bike.objects.filter(station_id=station_id)
            # print(bikes_available)

        # Serializing into json
        bikes_json = serialize('json', bikes_available)

        # Creating response object
        response = {'bikes': bikes_json, 'days': days[0], 'hours': hours[0]}
        
        # Sending response
        return JsonResponse(response)

def MakePayment(request):
    if request.is_ajax():
        bikeId = request.POST.get('bikeId', None)
        cost = request.POST.get('cost', None)
        payment_mode = request.POST.get('payment_mode', None)
        from_date = request.POST.get('from_date', None)
        to_date = request.POST.get('to_date', None)
        from_time = request.POST.get('from_time', None)
        to_time = request.POST.get('to_time', None)

        from_date, to_date, from_date_time, to_date_time = format_date(from_date, to_date, from_time, to_time)
        response = {}

        Bike = bike.objects.get(id=bikeId)

        payment = Payment.objects.create(customer=request.user, operator=Bike.operatorid, bike=Bike, station=Bike.station_id, amount=cost, mode=payment_mode)
        
        try:
            payment.save()
            bike_rent = BikeRentHistory.objects.create(customer=request.user, operator=Bike.operatorid, from_date_time=from_date_time, to_date_time=to_date_time, payment=payment, bike=Bike, station=Bike.station_id)

            bike_rent.save()
            response = {"message": "Your Bike has been successfully booked!"}
        except:
            response = {"message": "Failed to book Bike, please try again!"}
            
        return JsonResponse(response)


def format_date(from_date, to_date, from_time, to_time):
    from_time = from_time + ":00"
    to_time = to_time + ":00"

    # Combining date time
    from_date_time = datetime.strptime(from_date + ' ' + from_time, '%Y-%m-%d %H:%M:%S')
    to_date_time = datetime.strptime(to_date + ' ' + to_time, '%Y-%m-%d %H:%M:%S')
    
    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.strptime(to_date, '%Y-%m-%d')

    return (from_date, to_date, from_date_time, to_date_time)