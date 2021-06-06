from django.urls import path
from .views import home, register, customer_login

urlpatterns = [
    path('', view=home, name='CustomerHome'),
    path('register/', view=register, name='CustomerRegister'),
    path('login/', view=customer_login, name='CustomerLogin'),
]