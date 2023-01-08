from django import forms
from django.forms import ModelForm, TextInput, EmailInput, Textarea
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Name'
            }),
            'email': EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'Email'
            }),
            'body': Textarea(attrs={
                'class': "form-control",
                'placeholder': 'Message',
                'cols': 30,
                'rows': 5,
            }),
        }


class SearchForm(forms.Form):
    query = forms.CharField()
