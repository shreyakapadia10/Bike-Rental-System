from django.shortcuts import redirect, render
from .forms import *
from django.http import JsonResponse, HttpResponse
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_view
from .models import *
from django.core.serializers import serialize
import json
from django.views.generic import ListView, DetailView


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

class BikeAddView(CreateView):
    form_class = BikeRegistrationForm
    success_url = reverse_lazy('CustomerLogin')
    template_name = 'BikeUsers/bikeadd.html'
    

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
