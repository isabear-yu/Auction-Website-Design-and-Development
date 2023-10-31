from django import forms
from .models import Measurement

class MeasurementModelForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ('destination',)

class EditForm(forms.Form):
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'First Name'}))
    last_name  = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Last Name'}))
    age = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control',
               'placeholder': 'Age'}))
    address       = forms.CharField(max_length=200, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Address'}))
    city          = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'City'}))
    state         = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'State'}))
    zip_code      = forms.CharField(max_length=10, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Zip Code'}))
    phone_number = forms.CharField(max_length=16, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Phone Number'}))
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput(
        attrs={'class': 'form-control',
               'placeholder': 'Email'}))


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # We must return the cleaned data we got from our parent.
        return cleaned_data