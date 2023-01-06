from django.shortcuts import render
from .forms import ContactForm


def contact(response):
    template = 'contact.html'

    form = ContactForm()
    context = {'form': form}

    return render(response, template, context)
