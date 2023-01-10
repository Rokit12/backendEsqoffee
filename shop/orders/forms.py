from django.forms import ModelForm, TextInput
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import Order


class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city']
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'First Name'
            }),
            'last_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Last Name'
            }),
            'phone': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Phone'
            }),
            'email': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Email'
            }),
            'address': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Street name, house number',
            }),
            'postal_code': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Postal Code',
            }),
            'city': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'City',
            }),
        }
