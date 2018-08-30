from rest_framework import viewsets, mixins

from records.models import Record
from records.serializers import EndRecordSerializer


class EndRecordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Create a new Call End Record"""

    queryset = Record.objects.all()
    serializer_class = EndRecordSerializer
