from rest_framework import generics
from django.shortcuts import get_object_or_404

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
        for field in self.lookup_fields:
            if field in self.kwargs:
                filter[field] = self.kwargs[field]
        if 'period' in filter:
            obj = get_object_or_404(queryset, **filter)
        else:
            filter['period'] = '062018'
            obj = get_object_or_404(queryset, **filter)

        return obj


class BillViewSet(BillFieldsLookupMixin, generics.RetrieveAPIView):
    """Define a API endpoint for expose the Bill.

    Expose only the GET method for the API

    Attributes:
    subscriber(mandatory): the subscriber phone number. Format: AAXXXXXXXX(X)
        Where:
        AA - Area code
        XXXXXXXX(X) - Phone number with 8 or 9 digits
    period(optional): the bill month/year period reference Format: (MMYYYY)
        Where:
        MM - Month with 2 digits
        YYYY - Year with 2 digits
    """

    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    lookup_fields = ('subscriber', 'period')
