from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class StatusTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_status(self):
        response = self.client.get(('/api/status'))

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,{'status':'ok'})
