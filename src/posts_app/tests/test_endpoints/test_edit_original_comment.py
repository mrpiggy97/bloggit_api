#test success response, error response from permission
#and error response from bad data

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.models import Comment
from posts_app.tests.utils import (create_original_comment, create_post,
                                   create_sub, create_user)

import json

class TestEditOriginalComment(APITestCase):
    
    def setUp(self):
        
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)
        self.original_comment = create_original_comment(self.post, self.sub)
        
        self.client = APIClient()
        self.path = '/api/v1/posts/edit-original-comment/%s/' %(str(self.original_comment.uuid))
        self.data = json.dumps({
            'text': 'this is the updated text'
        })
        self.data_type = 'application/json'
    
    def test_success_response(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(path=self.path,
                                   data=self.data,
                                   content_type=self.data_type)
        status_code = status.HTTP_200_OK
        self.assertEqual(response.status_code, status_code)
        comment = Comment.objects.first()
        decoded_data = json.loads(self.data)
        self.assertEqual(comment.text, decoded_data.get('text'))
    
    def test_error_from_permission(self):
        response = self.client.put(path=self.path,
                                   data=self.data,
                                   content_type=self.data_type)
        status_code = status.HTTP_401_UNAUTHORIZED
        self.assertEqual(response.status_code, status_code)
    
    def test_error_from_bad_data(self):
        #when updating, post_uuid has to be None
        self.client.force_authenticate(self.user)
        bad_data = json.dumps({
            'post_uuid': str(self.post.uuid),
            'text': 'this is not supposed to work'
        })
        
        response = self.client.put(path=self.path,
                                   data=bad_data,
                                   content_type=self.data_type)
        status_code = status.HTTP_400_BAD_REQUEST
        expected_data = {
            'message': 'post_uuid must be None'
        }
        
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data, expected_data)
    
    def test_error_from_invalid_data(self):
        self.client.force_authenticate(self.user)
        invalid_data = json.dumps({
            'this is not supposed to work': 'this is not supposed to work'
        })
        response = self.client.put(path=self.path,
                                   data=invalid_data,
                                   content_type=self.data_type)
        status_code = status.HTTP_400_BAD_REQUEST
        expected_data = {
            'message': 'invalid data'
        }
        
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data, expected_data)