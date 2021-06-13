from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(to=State, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name 


class Customer(AbstractUser):
    STATUS_CHOICES = [('P', 'Pending'), ('V', 'Verified')]
    USER_CHOICES = [('C', 'Customer'), ('O', 'Operator')]

    email = models.EmailField(help_text='Enter your email id', unique=True)
    contact = models.IntegerField(help_text='Enter your contact number', null=True)
    address = models.CharField(max_length=200, help_text='Enter your address', null=True)
    pincode = models.IntegerField(help_text='Enter your pincode', null=True)
    proof = models.ImageField(upload_to='customer_proofs', help_text='Enter your identity proof', null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='P')
    role = models.CharField(('Select Your Role'), choices=USER_CHOICES, max_length=1, help_text='Select your role', null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, help_text='Select your state') 
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, help_text='Select your city')

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"

class bike(models.Model):
    BIKE_STATUS_CHOICES = [('A', 'Available'), ('R', 'Rent')] 
    operatorid = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, help_text='Enter operator id')
    bikename = models.CharField(max_length=50, help_text='Enter bike name')
    brandname = models.CharField(max_length=50, help_text='Enter bike brand name')
    price_hr = models.IntegerField(help_text='Enter bike price per hour')
    price_day = models.IntegerField(help_text='Enter bike price per day', null=True)
    registered_no = models.CharField(max_length=50, help_text='Enter bike registered number')
    bike_image=models.FileField(upload_to='bike_image', help_text='Add bike image', null=True)
    bike_manufactured_date=models.DateTimeField(help_text='Add Manufactured date of bike')
    bikecolor = models.CharField(max_length=50, help_text='Enter bike color')
    bikestatus = models.CharField(choices=BIKE_STATUS_CHOICES, max_length=1, default='A')
    station_id = models.IntegerField(help_text='Enter bike Station id')
    
    def __str__(self) -> str:
        return f" {self.bikename} ({self.brandname})"



class Rating(models.Model):
    suggestions=models.CharField(max_length=50, help_text='Enter your suggestion',default='Good')
    star = models.IntegerField(help_text='Add ratings')

    def __str__(self):
        return str(self.pk)

  


