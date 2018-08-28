from rest_framework import serializers

from records.models import Record


class EndRecordSerializer(serializers.ModelSerializer):
    """Serialize a End Call Record object

    Define the input fields and the output format
        of a End Call Record.
    The result of this serializations is displayed on the
        exposed API endpoints.
    """

    class Meta:
        model = Record
        fields = ('type', 'timestamp', 'call_id')
