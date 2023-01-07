from django.urls import path

from .views import (
    CreateContactAPIView
)

urlpatterns = [
    path('', CreateContactAPIView.as_view(), name="contact"),
]
