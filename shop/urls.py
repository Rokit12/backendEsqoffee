from django.urls import path, include
from .views import index, about, services

urlpatterns = [
    path('', index, name='home'),
    path('menu/', include('shop.products.urls', namespace='menu')),
    path('cart/', include('shop.cart.urls', namespace='cart')),
    path('orders/', include('shop.orders.urls', namespace='orders')),
    path('payment/', include('shop.payment.urls', namespace='payment')),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
]
