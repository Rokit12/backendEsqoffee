from django.urls import path, include
from .views import index

urlpatterns = [
    path('', index, name='home'),
    path('services', index, name='menu'),
    path('menu', index, name='menu'),
]
