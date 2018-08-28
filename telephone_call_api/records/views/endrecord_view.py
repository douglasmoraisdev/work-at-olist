from rest_framework import viewsets, mixins

from records.models import Record
from records.serializers import EndRecordSerializer


class EndRecordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Define a End Call Record View Set

    Define a API endpoint for expose the End Record.
    Expose only the POST method for the API by using the
        'CreateModelMixin' super class

    Attributes:
    queryset: Set a main entitie (Record)
    serializer_class: Set a Serializer for input and output fields
    """

    queryset = Record.objects.all()
    serializer_class = EndRecordSerializer
