from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from BikeUsers.forms import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from BikeUsers.models import *
from .models import *
from .forms import *


'''dashboard - This function based view is the dashboard for Operator, it requires user to be logged in'''
@login_required
def dashboard(request):
	if request.user.is_authenticated:
		if request.user.role == 'O':
			operator=request.user
			return render(request, 'BikeOperators/index.html', {'operator_name':operator })
		else:
			return redirect('CustomerHome')
	else:
		return redirect('CustomerLogin')


'''payment_details - This function based view will provide payment details of the given operator'''
@login_required
def payment_details(request):
	if request.user.is_authenticated:
		if request.user.role == 'O':
			PaymentHistory= Payment.objects.filter(operator=request.user)
			return render(request, 'BikeOperators/payment_details.html',{'payments':PaymentHistory})
		else:
			return redirect('CustomerHome')
	else:
		return redirect('CustomerLogin')


'''rent_history - This function based view will provide bike rent details of the given operator's bike'''
@login_required
def rent_history(request):
	if request.user.is_authenticated:
		if request.user.role == 'O':
			rentHistory= BikeRentHistory.objects.filter(operator=request.user)
			return render(request, 'BikeOperators/rented_bikes_history.html',{'rentHistory':rentHistory})
		else:
			return redirect('CustomerHome')
	else:
		return redirect('CustomerLogin')


'''operator_profile - This function based view can be used to update operator's profile'''
@login_required
def operator_profile(request):
	if request.method == 'POST':
		form = CustomerUpdateForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request,'Your Profile has been updated!')
			return redirect('profileUpdate')
		else:
			messages.error(request,'Please Enter Correct Information')
	else:
		form = CustomerUpdateForm(instance=request.user)

	context={'form': form}
	return render(request, 'BikeOperators/update_operator.html',context)


'''available_bikes - This function based view will return all the available bikes provided by that specific operator '''
@login_required	
def available_bikes(request):
	bikes= bike.objects.filter(operatorid=request.user, bikestatus='A')
	return render(request, 'BikeOperators/available_bikes.html',{'viewbike':bikes})


'''rented_bikes - This function based view will return all the rented bikes provided by that specific operator '''
@login_required
def rented_bikes(request):
	bikes= bike.objects.filter(operatorid=request.user, bikestatus='R')
	return render(request, 'BikeOperators/rented_bikes.html', {'viewbike': bikes }) 


'''all_bikes - This function based view will return all the bikes provided by that specific operator '''
@login_required
def all_bikes(request):
	bikes = bike.objects.filter(operatorid=request.user)
	return render(request=request, template_name='BikeOperators/all_bikes.html', context={'bikes': bikes})


'''BikeAddView - This class will require user to be logged in and allows the operator to add bike details, it uses bikeadd.html file as template and redirect user to the same page'''
class BikeAddView(LoginRequiredMixin, CreateView):
	form_class = BikeRegistrationForm
	success_url = reverse_lazy('BikeRegister')
	template_name = 'BikeOperators/bikeadd.html'
	success_message = 'Bike Details Added Successfully!'
	def form_valid(self, form):
		form.instance.operatorid = self.request.user
		messages.success(self.request, self.success_message)
		return super().form_valid(form)


'''BikeUpdateView - This class will require user to be logged in as well as it also checks that whether the user is eligible to update the bike details and allows the operator to update bike details, it uses bikeadd.html file as template and redirect user to the same page'''
class BikeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model=bike
	form_class = BikeUpdateForm
	success_url = reverse_lazy('BikeRegister')
	template_name = 'BikeOperators/bikeadd.html'
	success_message = 'Bike Details Updated Successfully!'
	def form_valid(self, form):
		form.instance.operatorid = self.request.user
		messages.success(self.request, self.success_message)
		return super().form_valid(form)

	def test_func(self):
		bike= self.get_object()

		if bike.operatorid == self.request.user:
			return True
		return False


'''BikeDeleteView - This class will require user to be logged in as well as it also checks that whether the user is eligible to delete the bike details and allows the operator to delete bike details, it uses bike_detail_confirm_delete.html file as template and redirect user to the login page'''
class BikeDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
	model=bike
	success_url = reverse_lazy('AllBikes')
	template_name = 'BikeOperators/bike_detail_confirm_delete.html'
	success_message = "Bike Details Deleted Successfully!"

	def delete(self, request, *args, **kwargs):
		messages.success(request=request, message=self.success_message)
		return super().delete(request, *args, **kwargs)

	def test_func(self):
		bike= self.get_object()

		if bike.operatorid == self.request.user:
			return True
		return False


'''AddStationView - This class based view is using MapsForm as form and it can be used to add new  bike station details, it uses add_station.html and redirects user to the same page'''
class AddStationView(CreateView):
	form_class = MapsForm
	template_name = 'BikeOperators/add_station.html'
	success_url = reverse_lazy('AddStation')
	success_message = 'Station Details Added Successfully!'

	def form_valid(self, form):
		messages.success(self.request, self.success_message)
		return super().form_valid(form)


'''add_station - This function accepts ajax POST request and if the form is valid the details will be saved or else error message will be sent in JSON, if the request is not ajax then it returns empty form'''
@login_required
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
		return render(request, 'BikeOperators/add_station.html', context)


'''update_status - This function based view will update the status of bike to available or on rent'''
@login_required
def update_status(request):
	if request.method == 'POST' and request.is_ajax():
		bike_id = request.POST.get('id')
		bike_status = request.POST.get('bike_status')

		response = {'message': ''}
		
		if bike_status == 'true':
			try:
				Bike = bike.objects.get(id=bike_id)
				Bike.bikestatus = 'A'
				Bike.save()
				response = {'message': 'Success'}
			except:
				response = {'message': 'Fail'}
		return JsonResponse(response)
	else:
		return redirect('RentedBikes')