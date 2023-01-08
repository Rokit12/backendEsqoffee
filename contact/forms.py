from django.forms import ModelForm, TextInput, EmailInput, Textarea
from .models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Name'
            }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'Email'
            }),
            'subject': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Subject'
            }),
            'message': Textarea(attrs={
                'class': "form-control",
                'placeholder': 'Message',
                'cols': 30,
                'rows': 5,
            }),
        }
