from django.forms import ModelForm, TextInput, ChoiceField, RadioSelect, Textarea

from .models import Order, Reservation

PAYMENT_OPTIONS = [
    ('cash', 'Cash'),
    ('mpesa', 'M-Pesa'),
    ('other', 'Card/Other'),
]
PICKUP_OPTIONS = [
    ('pickup', 'Pickup'),
    ('delivered', 'Delivery'),
]


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'First Name'
            }),
            'last_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Last Name'
            }),
            'date': TextInput(attrs={
                'class': "form-control appointment_date",
                'placeholder': 'Date'
            }),
            'time': TextInput(attrs={
                'class': "form-control appointment_time",
                'placeholder': 'Time'
            }),
            'phone': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Phone',
            }),
            'message': Textarea(attrs={
                'class': "form-control",
                'placeholder': 'Message',
                'cols': 30,
                'rows': 2,
            }),
        }


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
