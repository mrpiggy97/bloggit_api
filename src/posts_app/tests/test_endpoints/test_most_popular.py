#test most-popular endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.tests.utils import create_post, create_sub, create_user
from posts_app.models import Post

import json


class TestMostPopular(APITestCase):
    
    def setUp(self):
        self.user = create_user()
        self.sub = create_sub(self.user)
        #every community created with create_post has a community called test
        #by default
        self.path = '/posts/most-popular/{0}/'.format('test')
        self.client = APIClient()
        
        for n in range(0, 50):
            create_post(self.sub)
    
    
    def test_success_response(self):
        
        response = self.client.get(path=self.path)
        
        data = json.loads(response.data)
        
        #endpoint should return a paginated response with a count of 50
        self.assertEqual(data['count'], 50)
        self.assertEqual(response.status_code, status.HTTP_200_OK)