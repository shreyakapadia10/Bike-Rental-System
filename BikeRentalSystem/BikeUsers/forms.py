from django import forms
from .models import Customer


class CustomerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, help_text='Enter new password')
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'contact', 'address', 'pincode', 'email', 'password', 'proof']

    def __init__(self, *args, **kwargs):
        super(CustomerRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CustomerLoginForm(forms.ModelForm):
    email = forms.EmailField(help_text='Enter your email')
    password = forms.CharField(widget=forms.PasswordInput, help_text='Enter your password')

    class Meta:
        model = Customer
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(CustomerLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    USERNAME_FIELD = 'email'