from rest_framework import viewsets, mixins

from bills.models import Bill
from bills.serializers import BillSerializer


class BillViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Define a Bill View Set

    Define a API endpoint for expose the Bill.
    Expose only the GET method for the API by using the
        'ListModelMixin' super class

    Attributes:
    queryset: Set a main entitie (Bill)
    serializer_class: Set a Serializer for input and output fields
    """

    queryset = Bill.objects.all()
    serializer_class = BillSerializer
