#test creation and status code for bad data and permission denial

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.models import Comment
from posts_app.tests.utils import (create_post, create_original_comment,
                                   create_sub, create_user)

import json

class TestMakeChildComment(APITestCase):
    
    def setUp(self):
        
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)
        self.original_comment = create_original_comment(self.post, self.sub)
        
        self.client = APIClient()
        self.data = json.dumps({
            'commentfeed_uuid': str(self.original_comment.commentfeed.uuid),
            'owner_uuid': str(self.sub.uuid),
            'text': 'this is a child comment'
        })
        self.data_type = 'application/json'
        self.path = '/api/v1/posts/make-child-comment/'
    
    def test_success_response(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(path=self.path,
                                    data=self.data,
                                    content_type=self.data_type)
        status_code = status.HTTP_201_CREATED
        
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(response.status_code, status_code)
    
    def test_error_from_permission(self):
        response = self.client.post(path=self.path,
                                    data=self.data,
                                    content_type=self.data_type)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Comment.objects.count(), 1)
    
    def test_error_from_bad_data(self):
        self.client.force_authenticate(self.user)
        bad_data = {
            'commentfeed_uuid': None,
            'owner_uuid': str(self.sub.uuid),
            'text': 'this is not supposed to work'
        }
        response = self.client.post(path=self.path,
                                    data=bad_data,
                                    content_type=self.data_type)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 1)
    
    def test_error_from_invalid_data(self):
        '''test response from serializer recieveing invalid data'''
        self.client.force_authenticate(self.user)
        invalid_data = json.dumps({
            'this should return invalid response': 'this is not supposed to work'
        })
        status_code = status.HTTP_400_BAD_REQUEST
        
        expected_data = {
            'message': 'invalid data'
        }
        
        response = self.client.post(path=self.path,
                                    data=invalid_data,
                                    content_type=self.data_type)
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data, expected_data)