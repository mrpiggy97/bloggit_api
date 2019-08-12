#test most-popular endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.tests.utils import create_post, create_sub, create_user
from posts_app.models import Post

from taggit.models import Tag

import json


class TestMostPopular(APITestCase):
    
    def setUp(self):
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.community = Tag.objects.create(name='testing')
        self.path = '/posts/most-popular/%s/' %(self.community.slug)
        self.client = APIClient()
        
        for n in range(0, 50):
            create_post(self.sub)
    
    
    def test_success_response(self):
        
        response = self.client.get(path=self.path)
        posts = Post.objects.all()
        print("{0} {1}".format(response.data, posts.count()))
        self.assertEqual(response.status_code, status.HTTP_200_OK)