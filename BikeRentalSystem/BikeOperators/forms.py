from django import forms
from functools import partial
from BikeUsers.models import *

'''Add Bike Details Form'''
DateInput = partial(forms.DateInput, {'class': 'datepicker', 'autocomplete': 'off'})
class BikeRegistrationForm(forms.ModelForm):
    bike_manufactured_date = forms.DateField(widget=DateInput())
    class Meta:
        model = bike
        exclude=['operatorid']
        
    def __init__(self, *args, **kwargs):
        super(BikeRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['bike_manufactured_date'].widget.attrs.update({'class': 'datepicker form-control'})
    

'''Update Bike Form'''
DateInput = partial(forms.DateInput, {'class': 'datepicker', 'autocomplete': 'off'})
class BikeUpdateForm(forms.ModelForm):
    bike_manufactured_date = forms.DateField(widget=DateInput())
    class Meta:
        model = bike
        exclude=['operatorid', 'bikestatus']
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