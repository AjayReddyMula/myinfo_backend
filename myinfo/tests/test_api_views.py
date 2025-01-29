from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from myinfo.client import MyInfoPersonalClientV4

class MyInfoApiTests(APITestCase):

    @patch.object(MyInfoPersonalClientV4, 'get_authorise_url')
    def test_authorize_view_success(self, mock_get_authorise_url):
        """
        Test MyInfoAuthorizeView to ensure it returns the correct authorization URL.
        """
        callback_url = "http://localhost:8000/api/v1/myinfo/callback/"
        mock_get_authorise_url.return_value = (
            "http://mocked_authorize_url"
        )

        response = self.client.get(reverse('myinfo:authorize'), {"callback_url": callback_url})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('authorize_url', response.data)
        self.assertEqual(response.data['authorize_url'], "http://mocked_authorize_url")
        self.assertIn('state', response.data)

    def test_authorize_view_missing_callback_url(self):
        """
        Test MyInfoAuthorizeView when callback_url is missing.
        """
        response = self.client.get(reverse('myinfo:authorize'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'callback_url is required')

    @patch.object(MyInfoPersonalClientV4, 'retrieve_resource')
    def test_callback_view_success(self, mock_retrieve_resource):
        """
        Test MyInfoCallbackView to ensure it retrieves person data with valid parameters.
        """
        mock_retrieve_resource.return_value = {"person_name": "Clark Kent", "person_id": "12345"}
        response = self.client.get(reverse('myinfo:callback'), {"code": "mock_code", "state": "mock_state"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['person_name'], "Clark Kent")
        self.assertEqual(response.data['person_id'], "12345")

    def test_callback_view_invalid_payload(self):
        """
        Test MyInfoCallbackView when the payload is invalid.
        """
        response = self.client.get(reverse('myinfo:callback'), {"state": "state"})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_callback_view_missing_parameters(self):
        """
        Test MyInfoCallbackView when required parameters are missing.
        """
        response = self.client.get(reverse('myinfo:callback'), {"code": "code"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_callback_view_invalid_method(self):
        """
        Test MyInfoCallbackView to ensure GET requests are not allowed.
        """
        response = self.client.post(reverse('myinfo:callback'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'Method "POST" not allowed.')
