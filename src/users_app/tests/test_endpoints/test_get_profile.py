#test for get-profile endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.models import Post, Comment
from posts_app.serializers.PostSerializer import PostSerializer
from posts_app.serializers.CommentSerializer import CommentSerializer
from posts_app.tests.utils import create_post, create_sub, create_user

import json


class TestGetProfile(APITestCase):
    
    def setUp(self):
      
      self.user = create_user()
      self.sub = create_sub(self.user)
      self.path = '/users/profile/%s/' %(str(self.sub.uuid))
      self.client = APIClient()
      
      for n in range(0, 20):
          create_post(self.sub)
    
    def get_posts(self, authenticated):
        '''return serialized posts that belong to sub just created'''
        
        query = Post.objects.filter(owner=self.sub).order_by('-id')
        
        if authenticated == False:
            context = None
        else:
            context = {'session_sub': self.sub}
        
        posts = PostSerializer(query, context=context, many=True).data
        
        return posts
    
    def get_comments(self, authenticated):
        
        query = Comment.objects.filter(owner=self.sub)
        
        if authenticated == False:
            context = None
        else:
            context = {'session_sub': self.sub}
        
        comments = CommentSerializer(query, context=context, many=True).data
        
        return comments
    
    def test_success_response(self):
        
        #get a response that has a anonymous user
        anonymous_response = self.client.get(path=self.path)
        
        #make a response that has an authenticated user
        self.client.force_authenticate(user=self.user)
        authenticated_response = self.client.get(path=self.path)
        
        #this is the data expected as data from anonymous_response
        data = {
            'username': self.sub.get_username,
            'profile_picture': self.sub.get_profile_pic,
            'cake_day': self.sub.get_cake_day,
            'uuid': self.sub.get_uuid_as_string,
            'communities': self.sub.get_communities_as_list,
        }

        #this is the data expected as data from authenticated_response
        authenticated_data = data
        authenticated_data['authenticated'] = True
        authenticated_data['posts'] = self.get_posts(authenticated=True)
        authenticated_data['comments'] = self.get_comments(authenticated=True)
        json_authenticated_data = json.dumps(authenticated_data)
        
        #this is the data expected from and anonymous request
        anonymous_data = data
        anonymous_data['authenticated'] = False
        anonymous_data['posts'] = self.get_posts(authenticated=False)
        anonymous_data['comments'] = self.get_comments(authenticated=False)
        json_anonymous_data = json.dumps(anonymous_data)
        
        self.assertEqual(anonymous_response.status_code, status.HTTP_200_OK)
        self.assertTrue(anonymous_response.data == json_anonymous_data)
        
        self.assertEqual(authenticated_response.status_code, status.HTTP_200_OK)
        self.assertEqual(authenticated_response.data, json_authenticated_data)