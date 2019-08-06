#test for edit-post endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from django.contrib.auth.models import User

from posts_app.tests.utils import create_post, create_sub, create_user

import json


class TestEditPost(APITestCase):
    '''test edit-post endpoint'''

    def setUp(self):
        
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)

        self.path = '/posts/edit-post/%s/' %(str(self.post.uuid))
        self.client = APIClient()
        self.data = json.dumps({
            'title': 'edited title',
            'text': 'edited text',
            'owner_uuid': str(self.post.owner.uuid)
        })
    
    def test_success_response(self):

        self.client.force_authenticate(self.user)
        response = self.client.put(path=self.path, data=self.data, format='json')

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

        #now authenticate that new user
        self.client.force_authenticate(user=new_user)

        #make call
        response = self.client.put(path=self.path, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_error_response_from_bad_data(self):
        #test http response given when serializer is not valid

        bad_data = json.dumps({
            'title': 'new tle',
            'text': 'new text',
            'owner_uuid': None
        })

        self.client.force_authenticate(user=self.post.owner.user)
        response = self.client.put(path=self.path, data=bad_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)