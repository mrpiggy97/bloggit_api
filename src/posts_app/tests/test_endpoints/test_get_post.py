#test get-post endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.tests.utils import create_user, create_sub, create_post


class TestGetPost(APITestCase):
    '''test endpoint get-post/post_uuid/'''

    def setUp(self):

        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)

        self.path = '/api/v1/posts/get-post/%s/' %(str(self.post.uuid))

        self.client = APIClient()
    
    def test_response(self):
        
        response = self.client.get(path=self.path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_wrong_method_response(self):
        '''test what would happen if we made a request'''
        '''to self.path with the wrong method'''

        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)