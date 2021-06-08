from django.db import models
from django.contrib.auth.models import AbstractUser
from geoposition import Geoposition
from geoposition.fields import GeopositionField


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


class Station(models.Model):
    address = models.CharField(verbose_name="Address",max_length=100, null=True, blank=True)
    district = models.CharField(verbose_name="Town/City",max_length=100, null=True, blank=True)
    post_code = models.CharField(verbose_name="Post Code",max_length=8, null=True, blank=True)
    country = models.CharField(verbose_name="Country",max_length=100, null=True, blank=True)	
    longitude = models.CharField(verbose_name="Longitude",max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude",max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.address} ({self.post_code})'