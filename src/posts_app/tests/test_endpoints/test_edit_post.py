#test for edit-post endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from django.contrib.auth.models import User

from posts_app.models import Post
from posts_app.tests.utils import create_post, create_sub, create_user

import json


class TestEditPost(APITestCase):
    '''test edit-post endpoint'''

    def setUp(self):
        
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)

        self.path = '/api/v1/posts/edit-post/%s/' %(str(self.post.uuid))
        self.client = APIClient()
        self.data = json.dumps({
            'title': 'edited title',
            'text': 'edited text',
            'owner_uuid': str(self.sub.uuid)
        })
        self.invalid_data_response = {
            'message': 'sorry there was an error with the data provided'
        }
        self.data_type = 'application/json'
    
    def test_success_response(self):

        self.client.force_authenticate(self.user)
        response = self.client.put(path=self.path,
                                   data=self.data,
                                   content_type=self.data_type)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_error_response(self):
        '''test if we are granted permission if a'''
        '''user other than post.owner tries to edit the post'''

        #first we have to create a new user and a new sub
        #sub because PostView make a query to get the sub belonging
        #to that new user, there should always be a sub per user
        new_user = User.objects.create_user(
            username='otheruserqwe',
            password='newpassword47',
            email='newemail@mail.com'
        )
        new_sub = create_sub(new_user)

        #now authenticate that new user
        self.client.force_authenticate(user=new_user)

        #make call
        response = self.client.put(path=self.path,
                                   data=self.data,
                                   content_type=self.data_type)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_error_response_from_bad_data(self):
        #test http response given when serializer is not valid

        self.client.force_authenticate(self.post.owner.user)
        bad_data = json.dumps({
            'title': 'new tle',
        })
        response = self.client.put(path=self.path,
                                   data=bad_data,
                                   content_type=self.data_type)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)