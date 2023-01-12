from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_process, name='order_create'),
    path('reservation/', views.book_reservation, name='book_reservation'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
]
