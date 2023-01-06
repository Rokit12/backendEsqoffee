from django.conf.urls import url

from .views import (
    ListPostAPIView,
    DetailPostAPIView,
)

urlpatterns = [
    url(r'^$', ListPostAPIView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', DetailPostAPIView.as_view(), name='detail'),
]
