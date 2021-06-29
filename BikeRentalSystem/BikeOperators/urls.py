from django.urls import path
from django.urls.conf import include
from BikeUsers.views import SignIn
from .views import *

urlpatterns = [
    path('login/', view=SignIn.as_view(), name='OperatorLogin'),
    path('dashboard/', view=dash, name='OperatorDashboard'),
    path('available_bikes/',bikeinfo),
    path('rented_bikes/',bikeinfo1),
    
]