from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from functools import partial

'''User Registration Form'''
class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['role','first_name', 'last_name', 'username', 'contact', 'address', 'pincode', 'email', 'proof', 'state', 'city']

    def __init__(self, *args, **kwargs):
        super(CustomerCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

'''User Login Form'''
class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(help_text='Enter your username', required=True)

    class Meta:
        model = Customer
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(CustomerLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


'''Customer Change Form'''
class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        exclude = ('status', )


'''Add Bike Details Form'''
DateInput = partial(forms.DateInput, {'class': 'datepicker'})
class BikeRegistrationForm(forms.ModelForm):
    bike_manufactured_date = forms.DateField(widget=DateInput())
    bike_image=forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = bike
        exclude=['operatorid']
        
    def __init__(self, *args, **kwargs):
        super(BikeRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['bike_manufactured_date'].widget.attrs.update({'class': 'datepicker form-control'})
    

'''Update Bike Form'''
DateInput = partial(forms.DateInput, {'class': 'datepicker'})
class BikeUpdateForm(forms.ModelForm):
    bike_manufactured_date = forms.DateField(widget=DateInput())
    class Meta:
        model = bike
        exclude=['operatorid']
    def __init__(self, *args, **kwargs):
        super(BikeUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['bike_manufactured_date'].widget.attrs.update({'class': 'datepicker form-control'})


'''Add Station Form'''
class MapsForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=100, required=True)
    post_code = forms.CharField(max_length=8, required=True)
    country = forms.CharField(max_length=40, required=True)
    longitude = forms.CharField(max_length=50, required=True)
    latitude = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Station
        fields = ('name', 'address', 'city', 'post_code', 'country', 'longitude', 'latitude')

    def __init__(self, *args, **kwargs):
        super(MapsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


'''Select City Form'''
class CityForm(forms.ModelForm):
    CHOICES = (
        ("", "---------"),
    )

    name = forms.ChoiceField(required=True, choices=CHOICES, label="City", widget=forms.Select(attrs={'class': 'form-control'}))
    states = State.objects.all()
    state = forms.ModelChoiceField(queryset=states, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = City
        fields = ['state', 'name']

'''Customer Change Form'''
class CustomerUpdateForm(UserChangeForm):
    class Meta:
        model=Customer
        fields = ['role','first_name', 'last_name', 'username', 'contact', 'address', 'pincode', 'email', 'proof', 'state', 'city']

    def __init__(self, *args, **kwargs):
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'