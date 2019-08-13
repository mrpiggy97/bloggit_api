#test home endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.tests.utils import create_post, create_sub, create_user

class TestHomeView(APITestCase):
    
    def setUp(self):
        
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.path = '/posts/?page=1'
        self.client = APIClient()
        
        for n in range(0, 50):
            create_post(self.sub)
    
    def test_success_response(self):
        
        response = self.client.get(path=self.path)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)