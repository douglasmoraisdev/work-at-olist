from rest_framework import serializers

from records.models import Record


class StartRecordSerializer(serializers.ModelSerializer):
    """Serialize a Start Call Record object

    Define the input fields and the output format
        of a Start Call Record.
    The result of this serializations is displayed on the
        exposed API endpoints.
    """

    MAX_PHONE_NUMBER_SIZE = 11
    MIN_PHONE_NUMBER_SIZE = 10

    class Meta:
        model = Record
        fields = ('call_type', 'timestamp', 'call_id', 'source', 'destination')
        extra_kwargs = {
            'call_type': {
                'help_text': "Type of a Call Start Record (mandatory: 'S')"
            },
            'timestamp': {
                'help_text': "Date/time of a Call Start Record. "
                             "Format: YYYY-MM-DDThh:mm:ssZ"
            },
            'call_id': {
                'help_text': "Id of the Call Start Record. Makes a pair with "
                             "the a Call End Record"
            },
            'source': {
                'help_text': 'Phone number of the caller'
            },
            'destination': {
                'help_text': 'Phone number of the recipient'
            },
        }

    def is_valid_phone_number_size(self, value):

        return (self.MAX_PHONE_NUMBER_SIZE >= len(value)) and \
                self.MIN_PHONE_NUMBER_SIZE <= len(value)

    def validate_source(self, value):

        # Evaluates phone number format
        if not self.is_valid_phone_number_size(value):
            raise serializers.ValidationError("Wrong phone number format "
                                              "Expected AAXXXXXXX(X)"
                                              " with size from 10 to 11 "
                                              " characters")
        return value

    def validate_destination(self, value):

        # Evaluates phone number format
        if not self.is_valid_phone_number_size(value):
            raise serializers.ValidationError("Wrong phone number format "
                                              "Expected AAXXXXXXX(X)"
                                              " with size from 10 to 11 "
                                              " characters")
        return value
