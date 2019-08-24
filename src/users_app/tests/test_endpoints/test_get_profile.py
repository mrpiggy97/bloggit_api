#test for get-profile endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.tests.utils import create_post, create_sub, create_user

import json


class TestGetProfile(APITestCase):
    
    def setUp(self):
      
      self.user = create_user()
      self.sub = create_sub(self.user)
      self.path = '/users/get-profile/{0}'.format(self.sub.uuid)
      self.client = APIClient()
      
      for n in range(0, 20):
          create_post(self.sub)
    
    def test_success_response(self):
        
        #get a response that has a anonymous user
        anonymous_response = self.client.get(path=self.path)
        
        #make a response that has an authenticated user
        self.client.force_authenticate(user=self.user)
        authenticated_response = self.client.get(path=self.path)
        
        #this is the data expected as data from anonymous_response
        anonymous_data = json.dumps({
            'username': self.sub.get_username,
            'profile_picture': self.sub.get_profile_pic,
            'cake_day': self.sub.get_cake_day,
            'uuid': self.sub.get_uuid_as_string,
            'posts': posts,
            'comments': comments,
            'communities': self.sub.get_communities_as_list,
            'authenticated': False
        })

        #this is the data expected as data from authenticated_response
        authenticated_data = json.dumps({
            'username': self.sub.get_username,
            'profile_picture': self.sub.get_profile_pic,
            'cake_day': self.sub.get_cake_day,
            'uuid': self.sub.get_uuid_as_string,
            'posts': posts,
            'comments': comments,
            'communities': self.sub.get_communities_as_list,
            'authenticated': True
        })
        self.assertEqual(anonymous_response.status_code, status.HTTP_200_OK)
        self.assertEqual(authenticated_response.status_code, status.HTTP_200_OK)