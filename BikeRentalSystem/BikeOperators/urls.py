from django.urls import path
from django.urls.conf import include
from BikeUsers.views import *
from .views import *

urlpatterns = [
    path('login/', view=SignIn.as_view(), name='OperatorLogin'),
    path('dashboard/', view=dash, name='OperatorDashboard'),
    path('payment_details/',view=paymentDetailsView,name='payment'),
    path('rentedBike_details/',view=rentedBikeView,name='rentedBike'),
    path('update_customer/', view=OperatorUpdateView, name='profileUpdate'),
]