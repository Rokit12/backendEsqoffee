from django.forms import ModelForm, TextInput, ChoiceField, RadioSelect, BooleanField

from .models import Order

PAYMENT_OPTIONS = [
    ('cash', 'Cash'),
    ('mpesa', 'M-Pesa'),
    ('other', 'Card/Other'),
]
PICKUP_OPTIONS = [
    ('pickup', 'Pickup'),
    ('delivered', 'Delivery'),
]


class OrderCreateForm(ModelForm):
    payment_option = ChoiceField(
        widget=RadioSelect(attrs={'class': 'mr-2'}),
        choices=PAYMENT_OPTIONS,
    )
    pickup = ChoiceField(
        widget=RadioSelect(attrs={'class': 'mr-2'}),
        choices=PICKUP_OPTIONS,
    )

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city', 'payment_option',
                  'pickup']
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
