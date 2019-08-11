#test post-by-community endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from posts_app.tests.utils import create_post, create_sub, create_user
from posts_app.serializers.PostSerializer import PostSerializer
from posts_app.models import Post

from taggit.models import Tag

import json



class TestPostsByCommunity(APITestCase):
    '''test posts-by-community endpoint'''

    def setUp(self):

        #first create a user a sub and a couple of posts

        self.user = create_user()
        self.sub = create_sub(self.user)

        for n in range (0, 4):
            create_post(self.sub)
        
        for post in Post.objects.all():
            post.communities.add('test')
        
        self.path = '/posts/posts-by-community/%s/' %('test')
        self.client = APIClient()
        self.slug = 'test'
        self.serializer = PostSerializer
        self.paginator = PageNumberPagination()

    def test_success_response(self):
        #this request should be successful and return a 200 ok http response
        #along with a list of posts related to a community(tag)
        response = self.client.get(path=self.path)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)