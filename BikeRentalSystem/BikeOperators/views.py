from django.contrib import messages
from BikeUsers.forms import CustomerUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import *
from BikeUsers.models import *

# Create your views here.


@login_required
def dash(request):
	operator=request.user
	print(request.user)
	return render(request, 'BikeOperators/index.html', {'operator_name':operator })


@login_required
def paymentDetailsView(request):
	PaymentHistory= Payment.objects.filter(operator=request.user)
	return render(request, 'BikeOperators/payment_details.html',{'payments':PaymentHistory})


@login_required
def rentedBikeView(request):
	rentHistory= BikeRentHistory.objects.filter(operator=request.user)
	return render(request, 'BikeOperators/rentedBike.html',{'rentHistory':rentHistory})


@login_required
def OperatorUpdateView(request):
	if request.method == 'POST':
		form = CustomerUpdateForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request,'Your Profile has been updated!')
			return redirect('profileUpdate')
		else:
			messages.error(request,'Please Enter Correct')
	else:
		form = CustomerUpdateForm(instance=request.user)

	context={'form': form}
	return render(request, 'BikeOperators/update_operator.html',context)