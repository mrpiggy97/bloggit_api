from rest_framework.test import APIClient, APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from posts_app.tests.utils import create_sub, create_user

class TestInfo(APITestCase):
    
    def setUp(self):
        self.user = create_user()
        self.sub = create_sub(self.user)
        
        self.path = '/api/v1/users/profile-info/'
        self.client = APIClient()
    
    def test_success_response(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, HTTP_200_OK)
    
    def test_error_response_from_permission(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)