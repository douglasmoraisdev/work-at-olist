from rest_framework import viewsets, mixins

from records.models import Record
from records.serializers import StartRecordSerializer


class StartRecordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Create a new Call Start Record"""

    queryset = Record.objects.all()
    serializer_class = StartRecordSerializer
