from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer, State, City, bike, Station
from .forms import CustomerCreationForm, CustomerChangeForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Customer
    list_display = ['email', 'username',]

admin.site.register(Customer)
admin.site.register(State)
admin.site.register(City)
admin.site.register(bike)
admin.site.register(Station)