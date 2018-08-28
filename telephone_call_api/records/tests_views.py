from django.test import TestCase
from rest_framework.test import APIClient


class TestRecordEndPointsTestCase(TestCase):
    """Test Record Calls Endpoints behavior"""

    def setUp(self):
        self.client = APIClient()

    def test_start_record_endpoint_200_response(self):
        """Make a OPTIONS request to Start Record Call endpoint
        Expect a response 200 response (success)
        """

        request = self.client.options('/startrec/', {})

        self.assertEquals(request.status_code, 200)

    def test_end_record_endpoint_200_response(self):
        """Make a OPTIONS request to End Record Call endpoint
        Expect a response 200 response (success)
        """

        request = self.client.options('/endrec/', {})

        self.assertEquals(request.status_code, 200)
