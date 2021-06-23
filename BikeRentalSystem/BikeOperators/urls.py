from django.urls import path
from django.urls.conf import include
from BikeUsers.views import SignIn

urlpatterns = [
    path('login/', view=SignIn.as_view(), name='OperatorLogin'),
]