from django.test import TestCase
from rest_framework.test import APIClient


class TestRecordEndPointsTestCase(TestCase):
    """Test Record Calls Endpoints behavior"""

    def setUp(self):
        self.client = APIClient()

    def test_start_record_endpoint_options_200_response(self):
        """Make a OPTIONS request to Start Record Call endpoint
        Expect a response 200 response (success)
        """

        request = self.client.options('/startrec/', {})

        self.assertEquals(request.status_code, 200)

    def test_end_record_endpoint_options_200_response(self):
        """Make a OPTIONS request to End Record Call endpoint
        Expect a response 200 response (success)
        """

        request = self.client.options('/endrec/', {})

        self.assertEquals(request.status_code, 200)

    def test_start_record_endpoint_post_201_response(self):
        """Make a POST request to Start Record Call endpoint
        Expect a response 201 (created) response
        """

        _start_timestamp = "2018-08-26T15:07:10+0000"
        _end_timestamp = "2018-08-26T15:17:10+0000"
        _source = '51992657100'
        _destination = '5130232641'

        req = self.client.post('/startrec/', {'source': _source,
                                              'destination': _destination,
                                              'timestamp': _start_timestamp,
                                              'call_type': 'S',
                                              'call_id': 1
                                              })

        self.assertEquals(req.status_code, 201)

    def test_end_record_endpoint_post_201_response(self):
        """Make a POST request to End Record Call endpoint
        Expect a response 201 (success) response
        """
        _start_timestamp = "2018-08-26T15:07:10+0000"
        _end_timestamp = "2018-08-26T15:17:10+0000"
        _source = '51992657100'
        _destination = '5130232641'

        # first create a Start Call Record (origin)
        self.client.post('/startrec/', {'source': _source,
                                        'destination': _destination,
                                        'timestamp': _start_timestamp,
                                        'call_type': 'S',
                                        'call_id': 1
                                        })

        request = self.client.post('/endrec/', {'timestamp': _end_timestamp,
                                                'call_type': 'E',
                                                'call_id': 1
                                                })

        self.assertEquals(request.status_code, 201)

    def test_start_record_endpoint_get_405_response(self):
        """Make a GET request to Start Record Call endpoint
        Expect a response 405 (Method Not Allowed) response
        """

        request = self.client.get('/startrec/', {})

        self.assertEquals(request.status_code, 405)

    def test_end_record_endpoint_GET_405_response(self):
        """Make a GET request to End Record Call endpoint
        Expect a response 405 (Method Not Allowed) response
        """

        request = self.client.get('/endrec/', {})

        self.assertEquals(request.status_code, 405)

    def test_start_record_endpoint_delete_405_response(self):
        """Make a DELETE request to Start Record Call endpoint
        Expect a response 405 (Method Not Allowed) response
        """

        request = self.client.delete('/startrec/', {})

        self.assertEquals(request.status_code, 405)

    def test_end_record_endpoint_delete_405_response(self):
        """Make a DELETE request to End Record Call endpoint
        Expect a response 405 (Method Not Allowed) response
        """

        request = self.client.delete('/endrec/', {})

        self.assertEquals(request.status_code, 405)

    def test_start_record_endpoint_put_405_response(self):
        """Make a PUT request to Start Record Call endpoint
        Expect a response 405 (Method Not Allowed) response
        """

        request = self.client.put('/startrec/', {})

        self.assertEquals(request.status_code, 405)

    def test_end_record_endpoint_put_405_response(self):
        """Make a PUT request to End Record Call endpoint
        Expect a response 405 (Method Not Allowed) response
        """

        request = self.client.put('/endrec/', {})

        self.assertEquals(request.status_code, 405)
