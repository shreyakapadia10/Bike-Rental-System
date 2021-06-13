from django import forms
from .models import City, Customer, State, Station, bike
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

class CustomerCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, help_text='Enter your first name')
    last_name = forms.CharField(max_length=50, required=True, help_text='Enter your last name')

    class Meta:
        model = Customer
        fields = ['role','first_name', 'last_name', 'username', 'contact', 'address', 'pincode', 'email', 'proof', 'state', 'city']

    def __init__(self, *args, **kwargs):
        super(CustomerCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class BikeRegistrationForm(forms.ModelForm):
    class Meta:
        model = bike
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(BikeRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



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

class CustomerUpdateForm(UserChangeForm):
    class Meta:
        model=Customer
        fields=['email','contact']

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
