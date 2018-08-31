from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, ValidationError
from django.http import Http404

from bills.models import Bill
from bills.serializers import BillSerializer


class BillFieldsLookupMixin(object):
    """
    Filter the Bill queryset using the informed lookup fields on the
    BillViewSet class.
    Make 'period' field optional
    """
    def get_object(self):
        queryset = self.get_queryset()
        filter = {}

        # Get the lookup_fields to add to the queryset filter
        for field in self.lookup_fields:
            if field in self.kwargs:
                filter[field] = self.kwargs[field]

        # Assign default period id not informed
        if 'period' not in filter:
            filter['period'] = Bill().get_last_closed_period()

        # Return formated not found Bill Exception
        try:
            obj = get_object_or_404(queryset, **filter)
        except Http404:
            raise NotFound("Bill not found for "
                           "subscriber %s "
                           "on period %s/%s " %
                           (filter['subscriber'],
                            filter['period'][0:2], filter['period'][2:6])
                           )

        return obj


class BillSubscriberViewSet(BillFieldsLookupMixin, generics.RetrieveAPIView):
    """Get bill details of a subscriber on a given period"""

    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    lookup_fields = ('subscriber', 'period')


class BillLastPeriodViewSet(BillFieldsLookupMixin, generics.RetrieveAPIView):
    """Get last month bill details of a subscriber"""

    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    lookup_fields = ('subscriber', 'period')
