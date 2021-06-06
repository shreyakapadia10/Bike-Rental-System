from django.db import models

# Create your models here.
class Customer(models.Model):
   
    first_name = models.CharField(max_length=50, help_text='Enter your first name')
    last_name = models.CharField(max_length=50, help_text='Enter your last name')
    email = models.EmailField(unique=True, help_text='Enter your email id')
    contact = models.IntegerField(help_text='Enter your contact number')
    address = models.CharField(max_length=200, help_text='Enter your address')
    pincode = models.IntegerField(help_text='Enter your pincode')
    proof = models.ImageField(upload_to='customer_proofs', help_text='Enter your identity proof')
    status = models.TextField(default='Pending')
    password = models.CharField(max_length=50, help_text='Enter new password')
    # city_id = models.OneToOneField(City)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"