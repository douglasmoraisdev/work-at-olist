"""URL patterns for Start and End records endpoints
   defined on 'router' attribute
"""
from rest_framework import routers
from django.conf.urls import url, include

from records.views import StartRecordViewSet, EndRecordViewSet

router = routers.DefaultRouter()
router.register(r'startrec', StartRecordViewSet)
router.register(r'endrec', EndRecordViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
