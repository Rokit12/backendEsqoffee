from django.urls import path, include
from .views import index, about, services

urlpatterns = [
    path('', index, name='home'),
    path('menu/', include('shop.products.urls', namespace='menu')),
    path('cart/', include('shop.cart.urls', namespace='cart')),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
]
