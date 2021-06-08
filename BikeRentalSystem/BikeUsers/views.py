from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from .forms import CustomerCreationForm, CustomerLoginForm, MapsForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_view
import json
from django.http import HttpResponse

def home(request):
    if request.user.is_authenticated:
        return render(request, 'BikeUsers/maps.html')
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


class MapsView(CreateView):
    form_class = MapsForm
    template_name = 'BikeUsers/index.html'
    success_url = reverse_lazy('CustomerHome')


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
			message = "Station details added"
			context = {"result": result, "message": message,}
		else:
			context = {"result": result, "message": "error"}

		return HttpResponse(
			json.dumps(context),
			content_type="application/json"
			)
		
	context = {
		'up_form':up_form,
		}
	return render(request, 'BikeUsers/add_station.html', context)
