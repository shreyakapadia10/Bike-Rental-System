from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from functools import partial
from django.contrib.auth import authenticate, login

class CustomerCreationForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['role','first_name', 'last_name', 'username', 'contact', 'address', 'pincode', 'email', 'proof', 'state', 'city']

    def __init__(self, request, *args, **kwargs):
        super(CustomerCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.request = request

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            auth_user = authenticate(
                username=self.cleaned_data['username'], 
                password=self.cleaned_data['password1']
            )
            login(self.request, auth_user)

        return user

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

class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(help_text='Enter your username', required=True)

    class Meta:
        model = Customer
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(CustomerLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CustomerChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        exclude = ('status', )


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


class CustomerUpdateForm(UserChangeForm):
    class Meta:
        model=Customer
        fields=['email','contact']