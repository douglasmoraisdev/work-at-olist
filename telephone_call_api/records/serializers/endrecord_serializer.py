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
        fields = ('call_type', 'timestamp', 'call_id')
        extra_kwargs = {
            'call_type': {
                'help_text': "Type of a Call End Record (mandatory: 'E')"
            },
            'timestamp': {
                'help_text': "Date/time of a Call End Record. "
                             "Format: YYYY-MM-DDThh:mm:ssZ"
            },
            'call_id': {
                'help_text': 'Origin Id of the Call Start Record '
            }
        }

    def validate_call_type(self, value):

        # Evaluates call_type string
        if not value == 'E':
            raise serializers.ValidationError("Wrong call_type must be 'E'")
        return value
