from django.urls import path
from BikeUsers.views import *
from .views import *

urlpatterns = [
    path('', view=dashboard, name='OperatorDashboard'), # Operator Dashboard
    path('login/', view=SignIn.as_view(), name='OperatorLogin'), # Operator Login
    path('payment_details/', view=payment_details,name='payment'), # Payment Details
    path('rent_history/', view=rent_history,name='rentedBike'), # Bike Rent History
    path('profile/', view=operator_profile, name='profileUpdate'), # Operator Profile
    path('update_password/', view=PasswordChangeView, name='PasswordUpdate'), # To update password
    path('all_bikes/', all_bikes, name='AllBikes'), # All Bikes
    path('available_bikes/', available_bikes, name='AvailableBikes'), # Available Bikes
    path('rented_bikes/', rented_bikes, name='RentedBikes'), # Rented Bikes
    path('update_status/',update_status, name='UpdateBikeStatus'), # Update Bike Status
    path('add_station/', view=add_station, name='AddStation'), # Add Bike Station 
    path('add_bike/', view=BikeAddView.as_view(), name='BikeRegister'), # Add Bike
    path('bike/update/<int:pk>/', view=BikeUpdateView.as_view(), name='BikeUpdateView'), # Update Bike
    path('bike/delete/<int:pk>/', view=BikeDeleteView.as_view(), name='BikeDeleteView'), # Delete Bike
]