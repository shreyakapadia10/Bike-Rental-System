from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BikeRentHistory, Customer, Payment, State, City, bike, Rating,  Station
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
admin.site.register(Rating)
admin.site.register(Station)
admin.site.register(Payment)
admin.site.register(BikeRentHistory)
