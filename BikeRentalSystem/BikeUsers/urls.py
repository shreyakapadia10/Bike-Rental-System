from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('', view=home, name='CustomerHome'), # Home Page
    path('register/', view=SignUpView.as_view(), name='CustomerRegister'), # User Registration
    path('login/', view=SignIn.as_view(), name='CustomerLogin'), # User Login
    path('logout/', view=auth_view.LogoutView.as_view(template_name='BikeUsers/login.html'), name='CustomerLogout'), # User Logout
    path('update_customer/', CustomerUpdateView, name="ProfileUpdate"), # User Profile Update
    path('login_success/', login_success, name='login_success'),

    path('add_station', view=add_station, name='AddStation'), # Add Bike Station 
    path('addbike/', view=BikeAddView.as_view(), name='BikeRegister'), # Add Bike
    path('bike/update/<int:pk>/', view=BikeUpdateView.as_view(), name='Bike-UpdateView'), # Update Bike
    path('bike/delete/<int:pk>/', view=BikeDeleteView.as_view(), name='Bike-DeleteView'), # Delete Bike
    path('viewbike/<int:pk>',bikeinfo), # View Available Bikes of Selected Station
    path('bike/<int:pk>/',view=Bikedetails.as_view(),name='ShowBikeDetails'), # Show Bike Details
    path('history/', view_bike_history, name='ViewBikeHistory'), # Bike Rent History Page
    path('payment/',view=MakePayment, name='Payment'), # Bike Payment Page
    path('check_bikes/', check_bikes, name='CheckBikes'), # Supporting function to check available bikes
    
    path('feedback/', view=Rettingadd.as_view(), name='BikeFeedback'), # Feedback Page
    
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='BikeUsers/password/password_reset.html'), name='password_reset'), # Password Reset Page

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='BikeUsers/password/password_reset_done.html'), name='password_reset_done'), # Password Mail Sent Page
    
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='BikeUsers/password/password_reset_confirm.html'), name='password_reset_confirm'), # Password Reset Confirm Page
    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='BikeUsers/password/password_reset_complete.html'),name='password_reset_complete'), # Password Complete Page
    

    path('search_city/', view=search_city, name='SearchCity'), # Supporting function to get all citites of selected state
    path('search_station/', view=search_station, name='SearchStation'), # Supporting function to get all station names
    path('get_map/<int:pk>/', view=get_map, name='GetMap'), # Supporting function to get location details of selected station
]