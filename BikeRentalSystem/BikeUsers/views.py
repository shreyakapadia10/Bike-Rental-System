# Necessary imports
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, views as auth_view
from django.http import JsonResponse
from django.views.generic import DetailView
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from datetime import datetime


''' Home Page View - It will fetch stations details to show them to maps and render index.html file, along with that it returns stations and empty form for city based search if the user is logged in; else only returns empty city form'''
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


'''search_station function - This function accepts ajax request and will return list of stations based on whether the search is based on pincode or city, it returns JSON response'''
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
	success_url = reverse_lazy('CustomerHome')
	template_name = 'BikeUsers/login.html'
	success_message = 'Logged in successfully!'
	redirect_authenticated_user = True

	def form_valid(self, form):
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(self.request, username=username, password=password)
		if user.role == 'O':
			return redirect('OperatorDashboard')
		messages.success(self.request, self.success_message)
		return super().form_valid(form)


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


'''BikeAddView - This class will require user to be logged in and allows the operator to add bike details, it uses bikeadd.html file as template and redirect user to the same page'''
class BikeAddView(LoginRequiredMixin, CreateView):
	form_class = BikeRegistrationForm
	success_url = reverse_lazy('BikeRegister')
	template_name = 'BikeUsers/bikeadd.html'
	def form_valid(self, form):
		form.instance.operatorid = self.request.user
		return super().form_valid(form)


'''BikeUpdateView - This class will require user to be logged in as well as it also checks that whether the user is eligible to update the bike details and allows the operator to update bike details, it uses bikeadd.html file as template and redirect user to the same page'''
class BikeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model=bike
	form_class = BikeUpdateForm
	success_url = reverse_lazy('BikeRegister')
	template_name = 'BikeUsers/bikeadd.html'

	def form_valid(self, form):
		form.instance.operatorid = self.request.user
		return super().form_valid(form)

	def test_func(self):
		bike= self.get_object()

		if bike.operatorid == self.request.user:
			return True
		return False


'''BikeDeleteView - This class will require user to be logged in as well as it also checks that whether the user is eligible to delete the bike details and allows the operator to delete bike details, it uses bike_detail_confirm_delete.html file as template and redirect user to the login page'''
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

		if bike.operatorid == self.request.user:
			return True
		return False


'''Ratingadd - This class uses Ratings model and allows user to provide feedback, it requires user to be logged in, it uses feedback.html and redirects user to login page'''
class Rettingadd(LoginRequiredMixin, CreateView):
	model=Rating
	fields = '__all__'
	success_url = reverse_lazy('CustomerLogin')
	template_name = 'BikeUsers/feedback.html'
	success_message = 'Thank you for your valueable response!'

	def form_valid(self, form):
		messages.success(self.request, self.success_message)
		return super().form_valid(form)


'''AddStationView - This class based view is using MapsForm as form and it can be used to add new  bike station details, it uses add_station.html and redirects user to the same page'''
class AddStationView(CreateView):
	form_class = MapsForm
	template_name = 'BikeUsers/add_station.html'
	success_url = reverse_lazy('AddStation')


'''add_station - This function accepts ajax POST request and if the form is valid the details will be saved or else error message will be sent in JSON, if the request is not ajax then it returns empty form'''
def add_station(request):
	if request.is_ajax() and request.method == "POST":
		up_form = MapsForm(data = request.POST)

		#if both forms are valid, do something
		if up_form.is_valid():
			up_form.save()

			result = "perfect"
			message = "Station Details Added Successfully!"
			context = {"result": result, "message": message}
		else:
			result = "error"
			message = "Station Details Can't Be Added, Try again!"
			context = {"result": result, "message": message}

		return JsonResponse(context)

	else:
		up_form = MapsForm()
		context = {'up_form':up_form}
		return render(request, 'BikeUsers/add_station.html', context)


'''bikeinfo - This function based view is used to show bikes of a particularly selected bike stations, it renders viewbike.html and also returns list of bikes along with station id'''
def bikeinfo(request, pk):
	if request.user.is_authenticated:
		bikes=bike.objects.filter(station_id=pk)
		paginate_by = 2
		return render(request, 'BikeUsers/viewbike.html', {'viewbike': bikes, 'station': pk })
	return redirect('CustomerLogin')


'''Bikedetails - This class based view provides details of a particular bike and renders BikdeDetails.html'''
class Bikedetails(DetailView):
	model = bike
	template_name = 'BikeUsers/BikeDetails.html'


'''check_bikes - This function based views is used to provide a lits of available bikes based on user selected date and time duration, it accepts ajax request and returns JSON response, it requires user to be logged in'''
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
def view_bike_history(request):
	if request.user.is_authenticated:
		bike_rent_history = BikeRentHistory.objects.filter(customer=request.user)

		return render(request=request, template_name='BikeUsers/view_bike_history.html', context={'histories': bike_rent_history})

	return redirect('CustomerLogin')