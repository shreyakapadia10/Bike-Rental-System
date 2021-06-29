from django.db import models
from django.contrib.auth.models import AbstractUser

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
    first_name = models.CharField(max_length=50, help_text='Enter your first name')
    last_name = models.CharField(max_length=50, help_text='Enter your last name')
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
    name = models.CharField(verbose_name="Name",max_length=100, null=True, blank=True)
    address = models.CharField(verbose_name="Address",max_length=300, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, help_text='Select your city')
    post_code = models.CharField(verbose_name="Post Code",max_length=8, null=True, blank=True)
    country = models.CharField(verbose_name="Country",max_length=100, null=True, blank=True)	
    longitude = models.CharField(verbose_name="Longitude",max_length=50, null=True, blank=True)
    latitude = models.CharField(verbose_name="Latitude",max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}, {self.city} ({self.post_code})'


class bike(models.Model):
    BIKE_STATUS_CHOICES = [('A', 'Available'), ('R', 'On Rent')] 
    operatorid = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, help_text='Enter operator id')
    bikename = models.CharField(max_length=50, help_text='Enter bike name', verbose_name='Name of Bike')
    brandname = models.CharField(max_length=50, help_text='Enter bike brand name', verbose_name='Brand Name')
    price_hr = models.PositiveIntegerField(help_text='Enter bike price per hour', verbose_name='Price Per Hour')
    price_day = models.PositiveIntegerField(help_text='Enter bike price per day', null=True, verbose_name='Price Per Day')
    registered_no = models.CharField(max_length=50, help_text='Enter bike registered number', verbose_name='Bike Registration Number')
    bike_image=models.ImageField(upload_to='bike_image', help_text='Add bike image', null=True)
    bike_manufactured_date=models.DateField(help_text='Add Manufactured date of bike')
    bikecolor = models.CharField(max_length=50, help_text='Enter bike color', verbose_name='Bike Color')
    bikestatus = models.CharField(choices=BIKE_STATUS_CHOICES, max_length=1, default='A', verbose_name='Select Bike Status')
    station_id = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name='Select Station Location', help_text='Select Station Location')
    
    def __str__(self) -> str:
        return f" {self.bikename} ({self.brandname})"


class Rating(models.Model):
    suggestions=models.CharField(max_length=50, help_text='Enter your suggestion',default='Good')
    star = models.IntegerField(help_text='Add ratings')

    def __str__(self):
        return f'{self.suggestions} - {self.star} stars'


class Payment(models.Model):
    PAYMENT_CHOICES = [('COD', 'Cash On Delivery')]
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, related_name='customer+')
    operator = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, related_name='operator+')
    bike = models.ForeignKey(bike, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(choices=PAYMENT_CHOICES, max_length=3)

    def __str__(self) -> str:
        return f'{self.customer.first_name} paid - {self.amount} ({self.mode}) on {self.datetime} for bike {self.bike.bikename} of {self.operator.first_name}'


class BikeRentHistory(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, related_name='customer+')
    operator = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, related_name='operator+')
    from_date_time = models.DateTimeField(verbose_name='Select From Date Time:')
    to_date_time = models.DateTimeField(verbose_name='Select To Date Time:')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    bike = models.ForeignKey(bike, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.customer.first_name} rented {self.bike.bikename} - from {self.from_date_time} to {self.to_date_time} at {self.payment.amount} rupees'