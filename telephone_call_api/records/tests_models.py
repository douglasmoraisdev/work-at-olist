import datetime

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.exceptions import NotFound, ValidationError


from records.models import Record
from bills.models import Bill


class TestRecordModels(TestCase):
    """Test Record Calls Models behavior"""

    def test_save_record_S(self):
        """Save a S type call record"""

        _srecord = Record()
        _srecord.timestamp = datetime.datetime.strptime(
                                  "2018-08-26T15:07:10+0000",
                                  "%Y-%m-%dT%H:%M:%S%z")
        _srecord.source = '51992657100'
        _srecord.destination = '5133877079'
        _srecord.call_type = 'S'
        _srecord.call_id = '1'

        _srecord.save()

        self.assertEquals(Record.objects.filter(call_id=1).count(), 1)

    def test_save_record_E(self):
        """Save a E type call record"""

        _srecord = Record()
        _srecord.timestamp = datetime.datetime.strptime(
                                    "2018-08-26T15:07:10+0000",
                                    "%Y-%m-%dT%H:%M:%S%z")
        _srecord.source = '51992657100'
        _srecord.destination = '5133877079'
        _srecord.call_type = 'S'
        _srecord.call_id = '1'

        _srecord.save()

        _erecord = Record()
        _erecord.timestamp = datetime.datetime.strptime(
                                        "2018-08-26T16:16:13+0000",
                                        "%Y-%m-%dT%H:%M:%S%z")
        _erecord.call_type = 'E'
        _erecord.call_id = '1'

        _erecord.save()

        self.assertEquals(Record.objects.filter(call_id=1).count(), 2)

    def test_save_record_E_without_S_origin(self):
        """Save a E type call record without a S origin
        Expect fail (NotFound exception)
        """

        _srecord = Record()
        _srecord.timestamp = datetime.datetime.strptime(
                                                "2018-08-26T15:07:10+0000",
                                                "%Y-%m-%dT%H:%M:%S%z")
        _srecord.source = '51992657100'
        _srecord.destination = '5133877079'
        _srecord.call_type = 'S'
        _srecord.call_id = '1'

        _srecord.save()

        _ierecord = Record()
        _ierecord.timestamp = datetime.datetime.strptime(
                                                "2018-08-26T16:16:13+0000",
                                                "%Y-%m-%dT%H:%M:%S%z")
        _ierecord.call_type = 'E'
        _ierecord.call_id = '2'

        self.assertRaises(NotFound, lambda: _ierecord.save())
        self.assertNotEquals(Record.objects.filter(call_id=1).count(), 2)

    def test_save_record_Not_E_or_S(self):
        """Save a X type call record
        Expect fail (NotFound exception)
        """

        _srecord = Record()
        _srecord.timestamp = datetime.datetime.strptime(
                                                "2018-08-26T15:07:10+0000",
                                                "%Y-%m-%dT%H:%M:%S%z")
        _srecord.source = '51992657100'
        _srecord.destination = '5133877079'
        _srecord.call_type = 'X'
        _srecord.call_id = '1'

        self.assertRaises(ValidationError, lambda: _srecord.save())

    def test_save_record_E_lower_time_S(self):
        """Save a E type call record with timestamp lower than
        the S type call origin

        Expect fail (ValidationError exception)
        """

        _srecord = Record()
        _srecord.timestamp = datetime.datetime.strptime(
                                                "2018-08-26T15:07:10+0000",
                                                "%Y-%m-%dT%H:%M:%S%z")
        _srecord.source = '51992657100'
        _srecord.destination = '5133877079'
        _srecord.call_type = 'S'
        _srecord.call_id = '1'

        _srecord.save()

        _ierecord = Record()
        _ierecord.timestamp = datetime.datetime.strptime(
                                                "2018-08-26T14:16:13+0000",
                                                "%Y-%m-%dT%H:%M:%S%z")
        _ierecord.call_type = 'E'
        _ierecord.call_id = '1'

        self.assertRaises(ValidationError, lambda: _ierecord.save())
        self.assertNotEquals(Record.objects.filter(call_id=1).count(), 2)

    def test_save_record_E_already_closed(self):
        """Save a E type call record for a already ended call pair
        Expect fail (ValidationError exception)
        """

        _srecord = Record()
        _srecord.timestamp = datetime.datetime.strptime(
                                                "2018-08-26T15:07:10+0000",
                                                "%Y-%m-%dT%H:%M:%S%z")
        _srecord.source = '51992657100'
        _srecord.destination = '5133877079'
        _srecord.call_type = 'S'
        _srecord.call_id = '1'
        _srecord.save()

        _ierecord = Record()
        _ierecord.timestamp = datetime.datetime.strptime(
                                                 "2018-08-26T16:16:13+0000",
                                                 "%Y-%m-%dT%H:%M:%S%z")
        _ierecord.call_type = 'E'
        _ierecord.call_id = '1'
        _ierecord.save()

        _ierecord_2 = Record()
        _ierecord_2.timestamp = datetime.datetime.strptime(
                                                    "2018-08-26T16:26:13+0000",
                                                    "%Y-%m-%dT%H:%M:%S%z")
        _ierecord_2.call_type = 'E'
        _ierecord_2.call_id = '1'

        self.assertRaises(ValidationError, lambda: _ierecord_2.save())
        self.assertNotEquals(Record.objects.filter(call_id=1).count(), 3)

    def test_save_record_S_already_closed(self):
        """Save a S type call record for a already created
        S call record with same call_id
        Expect fail (ValidationError exception)
        """

        _srecord_1 = Record()
        _srecord_1.timestamp = datetime.datetime.strptime(
                                                    "2018-08-26T15:07:10+0000",
                                                    "%Y-%m-%dT%H:%M:%S%z")
        _srecord_1.source = '51992657100'
        _srecord_1.destination = '5133877079'
        _srecord_1.call_type = 'S'
        _srecord_1.call_id = '1'
        _srecord_1.save()

        _srecord_2 = Record()
        _srecord_2.timestamp = datetime.datetime.strptime(
                                                    "2018-08-28T15:07:10+0000",
                                                    "%Y-%m-%dT%H:%M:%S%z")
        _srecord_2.source = '51992657100'
        _srecord_2.destination = '51994355677'
        _srecord_2.call_type = 'S'
        _srecord_2.call_id = '1'

        self.assertRaises(ValidationError, lambda: _srecord_2.save())
        self.assertNotEquals(Record.objects.filter(call_id=1).count(), 2)

    def test_call_bill_period(self):
        """Save a call pair record and verify his bill period

        Should have to be the end call record date period
        """

        _srecord = Record()
        _srecord.timestamp = datetime.datetime.strptime(
                                    "2018-07-26T15:07:10+0000",
                                    "%Y-%m-%dT%H:%M:%S%z")
        _srecord.source = '51992657100'
        _srecord.destination = '5133877079'
        _srecord.call_type = 'S'
        _srecord.call_id = '1'

        _srecord.save()

        _erecord = Record()
        _erecord.timestamp = datetime.datetime.strptime(
                                        "2018-08-01T16:16:13+0000",
                                        "%Y-%m-%dT%H:%M:%S%z")
        _erecord.call_type = 'E'
        _erecord.call_id = '1'

        _erecord.save()

        self.assertEquals(Bill.objects.filter(subscriber='51992657100',
                                              period='082018').count(), 1)

    def test_save_record_S(self):
        """Save a S type call record with same source and destination
        Expect fail (ValidationError exception)
        """

        _srecord = Record()
        _srecord.timestamp = datetime.datetime.strptime(
                                  "2018-08-26T15:07:10+0000",
                                  "%Y-%m-%dT%H:%M:%S%z")
        _srecord.source = '51992657100'
        _srecord.destination = '51992657100'
        _srecord.call_type = 'S'
        _srecord.call_id = '1'

        self.assertRaises(ValidationError, lambda: _srecord.save())


class ManyBillsConsistencyTestCase(TestCase):

    def setUp(self):
        pass

    def test_many_subscribers_bills_in_same_month(self):

        # loop for create 40 subscribers
        _total_subs = 40
        while _total_subs > 0:
            _srecord = Record()
            _srecord.timestamp = datetime.datetime.strptime(
                                        "2018-07-26T15:07:10+0000",
                                        "%Y-%m-%dT%H:%M:%S%z")
            _srecord.source = '519926571%s' % str(_total_subs)
            _srecord.destination = '513387707%s' % str(_total_subs)
            _srecord.call_type = 'S'
            _srecord.call_id = _total_subs

            _srecord.save()

            _erecord = Record()
            _erecord.timestamp = datetime.datetime.strptime(
                                            "2018-08-01T16:16:13+0000",
                                            "%Y-%m-%dT%H:%M:%S%z")
            _erecord.call_type = 'E'
            _erecord.call_id = _total_subs

            _erecord.save()

            _total_subs = _total_subs - 1

        # loop for verify the 40 created bills
        _total_subs = 40
        while _total_subs > 0:
            self.assertEquals(Bill.objects.filter(
                                   subscriber='519926571%s' % str(_total_subs),
                                   period='082018').count(), 1
                              )
            _total_subs = _total_subs - 1
