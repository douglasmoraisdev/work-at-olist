from rest_framework import serializers

from records.models import Record


class StartRecordSerializer(serializers.ModelSerializer):
    """Serialize a Start Call Record object

    Define the input fields and the output format
        of a Start Call Record.
    The result of this serializations is displayed on the
        exposed API endpoints.
    """

    class Meta:
        model = Record
        fields = ('call_type', 'timestamp', 'call_id', 'source', 'destination')
