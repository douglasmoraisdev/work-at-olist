import time
import datetime
from datetime import timedelta
import json

from django.test import TestCase
from rest_framework.test import APIClient

from bills.models import Bill
from billrecords.models import BillRecord
from records.models import Record


class BillEndPointsTestCase(TestCase):
    """Test Bill Calls Endpoints behavior"""

    def setUp(self):
        self.client = APIClient()

    def test_bill_endpoint_options_200_response(self):
        """Make a OPTIONS request to Start Record Call endpoint
        Expect a response 200 response (success)
        """

        request = self.client.options('/bill/', {})

        self.assertEquals(request.status_code, 200)

    def test_bill_endpoint_get_200_response(self):
        """Make a GET request to Start Record Call endpoint
        Expect a response 200 response (success)
        """

        request = self.client.get('/bill/', {})

        self.assertEquals(request.status_code, 200)

    def test_bill_endpoint_post_405_response(self):
        """Make a POST request to Start Record Call endpoint
        Expect a response 405 (Method Not Allowed) response
        """

        request = self.client.post('/bill/', {})

        self.assertEquals(request.status_code, 405)

    def test_bill_endpoint_put_405_response(self):
        """Make a POST request to Start Record Call endpoint
        Expect a response 405 (Method Not Allowed) response
        """

        request = self.client.put('/bill/', {})

        self.assertEquals(request.status_code, 405)

    def test_bill_endpoint_delete_405_response(self):
        """Make a POST request to Start Record Call endpoint
        Expect a response 405 (Method Not Allowed) response
        """

        request = self.client.delete('/bill/', {})

        self.assertEquals(request.status_code, 405)


class BillFormatTestCase(TestCase):
    """Test Bill Calls Endpoints behavior"""

    def setUp(self):
        self.client = APIClient()

        # Create a Bill for tests
        _start_call = Record()
        _start_call.timestamp = datetime.datetime.strptime(
                                  "2018-08-26T15:07:10+0000",
                                  "%Y-%m-%dT%H:%M:%S%z")
        _start_call.source = '51992657100'
        _start_call.destination = '5133877079'
        _start_call.call_type = 'S'
        _start_call.call_id = '1'
        _start_call.save()

        _end_call = Record()
        _end_call.timestamp = datetime.datetime.strptime(
                                  "2018-08-26T15:17:10+0000",
                                  "%Y-%m-%dT%H:%M:%S%z")
        _end_call.call_type = 'E'
        _end_call.call_id = '1'
        _end_call.save()

        _start_period = _start_call.timestamp
        _end_period = _end_call.timestamp

        _bill = Bill()
        _bill.subscriber = '51992657100'
        _bill.period = '06/2018'
        _bill.save()

        _bill_record = BillRecord()
        _bill_record.bill_origin = _bill
        _bill_record.start_call = _start_call
        _bill_record.end_call = _end_call
        _bill_record.call_price = _bill.calculate_charge(
                                    _start_period, _end_period
                                  )
        _bill_record.save()

    def test_bill_endpoint_fields(self):
        """Test a output format (json) of a bill endpoint call"""

        request = self.client.get('/bill/', {})

        self.assertContains(request, 'id', status_code=200)
        self.assertContains(request, 'subscriber', status_code=200)
        self.assertContains(request, 'period', status_code=200)
        self.assertContains(request, 'calls_records', status_code=200)
        self.assertContains(request, 'destination', status_code=200)
        self.assertContains(request, 'call_start', status_code=200)
        self.assertContains(request, 'call_end', status_code=200)
        self.assertContains(request, 'call_duration', status_code=200)
        self.assertContains(request, 'call_price', status_code=200)
