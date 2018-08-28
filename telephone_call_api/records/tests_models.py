import datetime

from django.test import TestCase
from rest_framework.test import APIClient

from records.models import Record


class TestRecordModels(TestCase):
    """Test Record Calls Models behavior"""

    def test_start_record_insertion(self):
        """Make a INSERT into Record table (model)
        Expect a new row added (success)
        """

        _srecord = Record()
        _srecord.timestamp = datetime.datetime.strptime(
                                  "2018-08-26T15:07:10+0000",
                                  "%Y-%m-%dT%H:%M:%S%z")
        _srecord.source = '51992657100'
        _srecord.destination = '5133877079'
        _srecord.type = 'S'
        _srecord.call_id = '1'

        _srecord.save()

        self.assertEquals(Record.objects.filter(call_id=1).count(), 1)
