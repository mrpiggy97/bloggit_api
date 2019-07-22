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
        self.post = create_post(self.sub)

        self.path = '/posts/make-post/'
        self.client = APIClient()
        self.data = json.dumps({
            'title': 'this is a new post',
            'text': 'this is a new post',
            'owner_uuid': str(self.sub.uuid),
            'add_communities': ['test', 'first post']
        })
    
    def test_successful_creation(self):
        #this is how a call should be valid
        self.client.force_authenticate(user=self.sub.user)
        response = self.client.post(path=self.path, data=self.data, format='json')

        #we will test response status code and if indeed a post has been created

        post = Post.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.title, 'this is a new post')
    
    def test_error_response_from_permission(self):

        response = self.client.post(path=self.path, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)