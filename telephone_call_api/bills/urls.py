"""URL patterns for Bill endpoints
   defined on 'urlpatterns' attribute
"""
from django.conf.urls import url, include
from django.urls import path

from bills.views import BillSubscriberViewSet, BillLastPeriodViewSet

urlpatterns = [
    url('^bill/(?P<subscriber>.+)/(?P<period>.+)/$',
        BillSubscriberViewSet.as_view()),
    url('^bill/(?P<subscriber>.+)/$', BillLastPeriodViewSet.as_view()),
]
