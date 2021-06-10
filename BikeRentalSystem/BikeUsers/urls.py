from django.contrib import auth
from django.urls import path
from .views import SignIn, home, SignUpView, BikeAddView, add_station
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    path('', view=home, name='CustomerHome'),
    #path('',BikeListView.as_view() ,name='CustomerHome'),
    path('add_station', view=add_station, name='AddStation'),
    path('register/', view=SignUpView.as_view(), name='CustomerRegister'),
    path('login/', view=SignIn.as_view(), name='CustomerLogin'),
    path('logout/', view=auth_view.LogoutView.as_view(template_name='BikeUsers/login.html'), name='CustomerLogout'),
    path('bikeadd/', view=BikeAddView.as_view(), name='BikeRegister'),
    path('viewbike/',views.bikeinfo),
]