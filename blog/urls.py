from django.urls import path

from .views import (
    ListCategoryDetailAPIView,
    ListCategoryAPIView,
    ListPostAPIView,
    DetailPostAPIView,
)

urlpatterns = [
    path('', ListPostAPIView.as_view(), name="list"),
    path('<slug:slug>/detail/', DetailPostAPIView.as_view(), name="detail"),
    path('categories/', ListCategoryAPIView.as_view(), name="categories"),
    path('categories/<slug:slug>/', ListCategoryDetailAPIView.as_view(), name="category_detail"),
]
