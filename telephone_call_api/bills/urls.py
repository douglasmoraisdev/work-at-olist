"""URL patterns for Bill endpoints
   defined on 'urlpatterns' attribute
"""
from django.conf.urls import url, include
from django.urls import path

from bills.views import BillViewSet

urlpatterns = [
    url('^bill/(?P<subscriber>.+)/(?P<period>.+)/$', BillViewSet.as_view()),
    url('^bill/(?P<subscriber>.+)/$', BillViewSet.as_view()),
]
