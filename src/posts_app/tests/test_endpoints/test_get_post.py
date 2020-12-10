#test get-post endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.tests.utils import create_user, create_sub, create_post

from uuid import uuid4


class TestGetPost(APITestCase):
    '''test endpoint get-post/post_uuid/'''

    def setUp(self):

        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)

        self.path = '/api/v1/posts/get-post/%s/' %(str(self.post.uuid))

        self.fake_uuid = uuid4()
        self.path2 = "/api/v1/posts/get-post/%s/" %(str(self.fake_uuid))

        self.client = APIClient()
    
    def test_response(self):
        
        response = self.client.get(path=self.path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_wrong_method_response(self):
        '''test what would happen if we made a request'''
        '''to self.path with the wrong method'''

        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unfound_post(self):
        '''test the response we would get if'''
        '''a fake uuid was introduced in the url'''
        response = self.client.get(path=self.path2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)