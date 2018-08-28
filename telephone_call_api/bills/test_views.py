from django.test import TestCase
from rest_framework.test import APIClient


class TestBillEndPointsTestCase(TestCase):
    """Test Bill Calls Endpoints behavior"""

    def setUp(self):
        self.client = APIClient()

    def test_bill_endpoint__options_200_response(self):
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
