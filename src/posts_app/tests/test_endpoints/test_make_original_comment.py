#test if endpoint succesfully creates a comment that is original

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.models import Comment
from posts_app.serializers.CommentSerializer import OriginalCommentSerializer
from posts_app.tests.utils import (create_user, create_sub, create_post, create_post)

import json

class TestMakeOriginalComment(APITestCase):
    
    def setUp(self):
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)
        
        self.client = APIClient()
        self.path = '/posts/make-original-comment/'
        self.serializer = OriginalCommentSerializer
        self.data = json.dumps({
            'post_uuid': str(self.post.uuid),
            'owner_uuid': str(self.sub.uuid),
            'text': 'this is the comment'
        })
        self.data_type = 'application/json'
    
    def test_success_response(self):
        '''only authenticated requests should have permission''' 
        self.client.force_authenticate(self.user)
        response = self.client.post(path=self.path,
                                    data=self.data,
                                    content_type=self.data_type)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
    
    def test_error_from_permission(self):
        '''test if tbe error code is the expected'''
        response = self.client.post(path=self.path,
                                    data=self.data,
                                    content_type=self.data_type)
        code = status.HTTP_401_UNAUTHORIZED
        self.assertEqual(response.status_code, code)
        self.assertEqual(Comment.objects.count(), 0)
    
    def test_error_from_bad_data(self):
        '''test if error code is correct if data is not good'''
        self.client.force_authenticate(self.user)
        bad_data = json.dumps({
            'post_uuid': None,
            'owner_uuid': str(self.sub.uuid),
            'text': 'this is not supposed to work'
        })
        response = self.client.post(path=self.path,
                                    data=bad_data,
                                    content_type=self.data_type)
        
        code = status.HTTP_400_BAD_REQUEST
        self.assertEqual(response.status_code, code)
    
    def test_error_from_invalid_data(self):
        self.client.force_authenticate(self.user)
        invalid_data = json.dumps({
            'this is not supposed to work': 'this is not supposed to work'
        })
        status_code = status.HTTP_400_BAD_REQUEST
        expected_data = {
            'message': 'invalid data'
        }
        response = self.client.post(data=invalid_data,
                                    path=self.path,
                                    content_type=self.data_type)
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data, expected_data)