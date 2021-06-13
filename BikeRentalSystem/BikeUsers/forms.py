from django import forms
from .models import Customer, bike
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from functools import partial


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


# class CustomerRegisterForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, help_text='Enter new password')
#     class Meta:
#         model = Customer
#         fields = ['first_name', 'last_name', 'contact', 'address', 'pincode', 'email', 'password', 'proof']

#     def __init__(self, *args, **kwargs):
#         super(CustomerRegisterForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'


# class CustomerLoginForm(forms.ModelForm):
#     email = forms.EmailField(help_text='Enter your email')
#     password = forms.CharField(widget=forms.PasswordInput, help_text='Enter your password')

#     class Meta:
#         model = Customer
#         fields = ['email', 'password']

#     def __init__(self, *args, **kwargs):
#         super(CustomerLoginForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'

#     USERNAME_FIELD = 'email'