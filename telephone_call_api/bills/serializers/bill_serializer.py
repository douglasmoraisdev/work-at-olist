from rest_framework import serializers

from bills.models import Bill


class BillSerializer(serializers.ModelSerializer):
    """Serialize a Bill object

    Define the input fields and the output format
        of a Bill.
    The result of this serializations is displayed on the
        exposed API endpoints.
    """

    class Meta:
        model = Bill
        fields = ('id', 'subscriber', 'period')
