#test make-post endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.tests.utils import create_post, create_sub, create_user
from posts_app.models import Post

import json


class TestMakePost(APITestCase):
    '''testing make-post endpoint'''

    def setUp(self):

        self.user = create_user()
        self.sub = create_sub(self.user)

        self.path = '/api/v1/posts/make-post/'
        self.client = APIClient()
        self.data = json.dumps({
            'title': 'this is a new post',
            'text': 'this is a new post',
            'add_communities': ['test', 'first post']
        })
        self.data_type = 'application/json'
    
    def test_success_response(self):
        #this is how a call should be valid
        self.client.force_authenticate(user=self.sub.user)
        response = self.client.post(path=self.path,
                                    data=self.data,
                                    content_type=self.data_type)

        #we will test response status code and if indeed a post has been created

        post = Post.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.title, 'this is a new post')
    
    def test_response_from_permission(self):

        response = self.client.post(path=self.path,
                                    data=self.data,
                                    content_type=self.data_type)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)
    
    def test_response_from_invalid_data(self):
        self.client.force_authenticate(self.user)
        invalid_data = json.dumps({
            'tite': 'this is the title',
            'text': 'this is the text',
            'communities': ['test'],
        })
        
        response = self.client.post(path=self.path,
                                    data=invalid_data,
                                    content_type=self.data_type)
        
        status_code = status.HTTP_400_BAD_REQUEST
        expected_data = {
            'message': 'invalid data'
        }
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(Post.objects.count(), 0)