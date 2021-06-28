from django.contrib import messages
from BikeUsers.forms import CustomerUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import *
from BikeUsers.models import *
from django.views.generic import ListView

# Create your views here.



def dash(request):
	operator= request.user
	return render(request, 'BikeOperators/index.html',{'operator_name':operator })

def paymentDetailsView(request):
	PaymentHistory= Payment.objects.filter(operator=request.user)
	return render(request, 'BikeOperators/payment_details.html',{'payments':PaymentHistory})


def rentedBikeView(request):
	#print(request.user.id)
	rentHistory= BikeRentHistory.objects.filter(operator=request.user)
	return render(request, 'BikeOperators/rentedBike.html',{'posts':rentHistory})

@login_required
def OperatorUpdateView(request):
    if request.method == 'POST':
        u_form = CustomerUpdateForm(request.POST,instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request,'Your Profile has been updated!')
            return redirect('profileUpdate')
        else:
             messages.error(request,'Please Enter Correct')
    else:
        u_form = CustomerUpdateForm(instance=request.user)

    context={ 'u_form': u_form}
    return render(request, 'BikeOperators/update_operator.html',context)

