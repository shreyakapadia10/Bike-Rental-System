from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm

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
        model = Customer
        fields = ['first_name', 'last_name', 'username', 'contact', 'address', 'pincode', 'email', 'proof', 'state', 'city']

    def __init__(self, *args, **kwargs):
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class PasswordUpdateForm(PasswordChangeForm):
    class Meta:
        model = Customer

    def __init__(self, user, *args, **kwargs):
        super(PasswordUpdateForm, self).__init__(user, *args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'