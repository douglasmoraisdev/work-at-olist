from rest_framework import viewsets, mixins

from records.models import Record
from records.serializers import StartRecordSerializer


class StartRecordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Define a Start Call Record View Set

    Define a API endpoint for expose the Start Record.
    Expose only the POST method for the API by using the
        'CreateModelMixin' super class

    Attributes:
    queryset: Set a main entitie (Record)
    serializer_class: Set a Serializer for input and output fields
    """

    queryset = Record.objects.all()
    serializer_class = StartRecordSerializer
