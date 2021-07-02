# Necessary imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.api import success
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, update_session_auth_hash, views as auth_view
from django.http import JsonResponse, request
from django.views.generic import DetailView
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from datetime import datetime


''' Home Page View - It will fetch stations details to show them to maps and render index.html file, along with that it returns stations and empty form for city based search if the user is logged in; else only returns empty city form'''
def home(request):
	if request.user.is_authenticated:
		if request.user.role == 'C':
			stations = Station.objects.all()
			if len(stations) > 0:
				station_json = serialize('json', stations)
				form = CityForm()
				return render(request, 'BikeUsers/index.html', {'stations': station_json, 'form': form})
			else:
				form = CityForm()
				return render(request, 'BikeUsers/index.html', {'stations': '', 'form': form})
		else:
			return redirect('OperatorDashboard')
	else:
		return redirect('CustomerLogin')


'''search_station function - This function accepts ajax request and will return list of stations based on whether the search is based on pincode or city, it returns JSON response'''
@login_required
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


'''search_city - This function accepts ajax request and will return cities for the selected state in JSON format'''
@login_required
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


'''get_map - This function gets id of particular station and renders get_map.html file, along with that it returns station details so that the direction to the station can be shown'''
@login_required
def get_map(request, pk):
	station = Station.objects.get(id=pk)
	station_json = serialize('json',[station])
	return render(request=request, template_name='BikeUsers/get_map.html', context={'station': station_json})


'''SignUpView - This class based view is used for user registration, it uses register.html and upon successful registration it redirects to login page'''
class SignUpView(CreateView):
	form_class = CustomerCreationForm
	template_name = 'BikeUsers/register.html'
	success_message = 'Registered Successfully!'

	def form_valid(self, form):
		#save the new user first
		form.save()
		messages.success(self.request, self.success_message)
		#get the username and password
		username = self.request.POST['username']
		password = self.request.POST['password1']
		#authenticate user then login
		user = authenticate(username=username, password=password)
		login(self.request, user)
		return redirect('CustomerHome')

'''SignIn - This class based view is used for user login, it uses login.html and upon successful login it redirects to home page, also if the user is authenticated the it redirects user to home page automatically'''
class SignIn(auth_view.LoginView):
	form_class = CustomerLoginForm
	# success_url = reverse_lazy('CustomerHome')
	template_name = 'BikeUsers/login.html'
	success_message = 'Logged in successfully!'
	# redirect_authenticated_user = True


	def form_valid(self, form):
		messages.success(self.request, self.success_message)
		return super().form_valid(form)


'''login_success - This function based view redirects users based on whether they are Customer or Operator'''
@login_required
def login_success(request):
	if request.user.is_authenticated:
		# If user is a Customer
		if request.user.role == 'C': 
			return redirect('CustomerHome')
		# If user is an Operator
		else:
			return redirect('OperatorDashboard')
	else:
		return redirect('CustomerLogin')

'''CustomerUpdateView - This function based view is used to update user details, it requires the user to be logged in and if the form details are valid then it'll update user details and redirect user to Home page, it renders update_customer.html'''
@login_required
def CustomerUpdateView(request):
	if request.method == 'POST':
		u_form = CustomerUpdateForm(request.POST, request.FILES, instance=request.user)
		
		if u_form.is_valid():
			u_form.save()
			messages.success(request,'Your Profile has been updated successfully!')
			return redirect('ProfileUpdate')
	else:
		u_form = CustomerUpdateForm(instance=request.user)

	context={ 'u_form': u_form}
	return render(request, 'BikeUsers/update_customer.html',context)


'''Ratingadd - This class uses Ratings model and allows user to provide feedback, it requires user to be logged in, it uses feedback.html and redirects user to login page'''
@login_required
def Rettingadd(request, pk):
	if request.method=="POST":
		star = request.POST.get('star')
		suggestions = request.POST.get('suggestions')

		if star is not None and suggestions != '':
			try:
				Bike = bike.objects.get(id=pk)
				new_rating = Rating.objects.create(star=star, suggestions=suggestions, bike=Bike, customer=request.user)
				new_rating.save()
				messages.success(request, 'Thank you for your valuable feedback!')
				return redirect('ViewBikeHistory')
			except:
				return render(request,'BikeUsers/feedback.html')
		else:
			messages.warning(request, 'Please provide valid feedback!')
	return render(request,'BikeUsers/feedback.html')

'''bikeinfo - This function based view is used to show bikes of a particularly selected bike stations, it renders viewbike.html and also returns list of bikes along with station id'''
@login_required
def bikeinfo(request, pk):
	if request.user.is_authenticated:
		bikes=bike.objects.filter(station_id=pk)
		return render(request, 'BikeUsers/viewbike.html', {'viewbike': bikes, 'station': pk })
	return redirect('CustomerLogin')


'''Bikedetails - This class based view provides details of a particular bike and renders BikdeDetails.html'''
class Bikedetails(DetailView):
	model = bike
	template_name = 'BikeUsers/BikeDetails.html'


'''check_bikes - This function based views is used to provide a lits of available bikes based on user selected date and time duration, it accepts ajax request and returns JSON response, it requires user to be logged in'''
@login_required
def check_bikes(request):
	if request.user.is_authenticated:
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
			minutes = divmod(hours[1], 60) # Use remainder of hours to calc minutes

			# Getting bikes which are on rent on given date and time of particular station
			filter_params = dict(from_date_time__lt=to_date_time, to_date_time__gt=from_date_time) # Providing filter condtions

			bike_rent_history = BikeRentHistory.objects.filter(**filter_params, station=station_id)

			# if queryset is not empty
			if len(bike_rent_history) > 0:
				# Excluding bikes which are on rent
				bikes_available = bike.objects.exclude(id__in=bike_rent_history.values_list('bike_id', flat=True))

			# If no such bikes find between given date and time range
			else:
				bikes_available = bike.objects.filter(station_id=station_id)

			# Serializing into json
			bikes_json = serialize('json', bikes_available)

			# Creating response object
			response = {'bikes': bikes_json, 'days': days[0], 'hours': hours[0], 'minutes': minutes[0]}

			# Sending response
			return JsonResponse(response)
	return redirect('CustomerLogin')


'''MakePayment - This function based view accepts ajax request, it requires user to be logged in and saves payment details and bike history details and returns JSON response'''
@login_required
def MakePayment(request):
	if request.user.is_authenticated:
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

			try:
				Bike = bike.objects.get(id=bikeId)
				Bike.bikestatus = 'R'
				Bike.save()
				payment = Payment.objects.create(customer=request.user, operator=Bike.operatorid, bike=Bike, station=Bike.station_id, amount=cost, mode=payment_mode)

				payment.save()
				bike_rent = BikeRentHistory.objects.create(customer=request.user, operator=Bike.operatorid, from_date_time=from_date_time, to_date_time=to_date_time, payment=payment, bike=Bike, station=Bike.station_id)

				bike_rent.save()
				response = {"message": "Your Bike has been successfully booked!"}
			except:
				response = {"message": "Failed to book Bike, please try again!"}

			return JsonResponse(response)
	return redirect('CustomerLogin')


'''format_date - This helper function is used to format the date and time, it accepts two dates and two time strings, it combines date and time, converts date into python object and returns combined datetime and formatted dates'''
def format_date(from_date, to_date, from_time, to_time):
	# Combining date time
	from_date_time = datetime.strptime(from_date + ' ' + from_time, '%Y-%m-%d %H:%M')
	to_date_time = datetime.strptime(to_date + ' ' + to_time, '%Y-%m-%d %H:%M')

	from_date = datetime.strptime(from_date, '%Y-%m-%d')
	to_date = datetime.strptime(to_date, '%Y-%m-%d')

	return (from_date, to_date, from_date_time, to_date_time)


'''view_bike_history - This function based view is used to show bike rent history of the logged in user, it renders view_bike_history.html along with it, it returns all rented bikes. It requires the user to be logged in'''
@login_required
def view_bike_history(request):
	if request.user.is_authenticated:
		bike_rent_history = BikeRentHistory.objects.filter(customer=request.user)

		return render(request=request, template_name='BikeUsers/view_bike_history.html', context={'histories': bike_rent_history})

	return redirect('CustomerLogin')


'''PasswordChangeView'''
@login_required
def PasswordChangeView(request):
	
	if request.method == "POST":
		form = PasswordUpdateForm(request.user, request.POST)

		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request=request, message='Your password has been successfully updated!')
			return redirect('CustomerHome')
		else:
			messages.warning(request=request, message='Please check your password!')

	form = PasswordUpdateForm(request.user)
	if request.user.role == 'C':
		return render(request=request, template_name='BikeUsers/password_update.html', context={'form': form})
	return render(request=request, template_name='BikeOperators/password_update.html', context={'form': form})
