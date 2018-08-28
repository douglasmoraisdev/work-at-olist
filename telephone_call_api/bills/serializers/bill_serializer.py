from rest_framework import serializers

from bills.models import Bill


class BillSerializer(serializers.ModelSerializer):
    """Serialize a Bill object

    Define the input fields and the output format
        of a Bill.
    The result of this serializations is displayed on the
        exposed API endpoints.
    """

    calls_records = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = ('id', 'subscriber', 'period', 'calls_records')

    def get_calls_records(self, bill):
        """Define the format for bill call records list output"""

        _calls_records_list = []

        # Get all bill records from the bill
        for _recs in bill.billrecord_set.all():

            # Calculate the call duration for output
            _duration = _recs.end_call.timestamp - _recs.start_call.timestamp
            _seconds = int(_duration.total_seconds() % 60)
            _minutes = int(_duration.total_seconds() % 3600 // 60)
            _hours = int(_duration.total_seconds() // 3600)

            # Format the call duration for output
            _duration_formated = '%sh%sm%ss' % (_hours, _minutes, _seconds)

            # Format the call record and add to return list
            _calls_records_data = {
                'destination': _recs.end_call.destination,
                'call_start': _recs.start_call.timestamp,
                'call_end': _recs.end_call.timestamp,
                'call_duration': _duration_formated,
                'call_price': "R$%6.2f" % _recs.call_price
            }
            _calls_records_list.append(_calls_records_data)

        return _calls_records_list
