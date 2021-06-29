from django.shortcuts import render
from  BikeUsers.models import *
from .forms import *
# Create your views here.



def dash(request):
	return render(request, 'BikeOperators/index.html')

def bikeinfo(request):
	#print(request.user.id)
	bikes= bike.objects.filter(operatorid=request.user)

	return render(request, 'BikeOperators/available_bikes.html',{'viewbike':bikes})


def bikeinfo1(request):
	bikes= bike.objects.filter(operatorid=request.user)
	return render(request, 'BikeOperators/rented_bikes.html', {'viewbike': bikes }) 
