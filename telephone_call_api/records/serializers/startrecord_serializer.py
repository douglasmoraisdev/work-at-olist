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

    def is_valid_phone_number_size(self, value):

        return (self.MAX_PHONE_NUMBER_SIZE >= len(value)) and \
                self.MIN_PHONE_NUMBER_SIZE <= len(value)

    def validate_source(self, value):

        # Evaluates phone number format
        if not self.is_valid_phone_number_size(value):
            raise serializers.ValidationError("Wrong phone number format\n\
                                              Expected AAXXXXXXX(X)\
                                              10 to 11 size number")
        return value

    def validate_destination(self, value):

        # Evaluates phone number format
        if not self.is_valid_phone_number_size(value):
            raise serializers.ValidationError("Wrong phone number format\n\
                                              Expected AAXXXXXXX(X)\
                                              10 to 11 size number")
        return value
