"""URL patterns for Bill endpoints
   defined on 'router' attribute
"""
from rest_framework import routers
from django.conf.urls import url, include

from bills.views import BillViewSet

router = routers.DefaultRouter()
router.register(r'bill', BillViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
