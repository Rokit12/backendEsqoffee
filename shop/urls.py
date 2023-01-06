from django.urls import path
from .views import index, about, contact, services

urlpatterns = [
    path('', index, name='home'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('services', services, name='services'),
]
