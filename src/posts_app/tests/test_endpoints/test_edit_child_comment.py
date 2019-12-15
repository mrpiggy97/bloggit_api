#test successful response, error response from invalid data
#permission and bad data

from rest_framework.test import APIClient, APITestCase
from rest_framework.status import (HTTP_200_OK, HTTP_401_UNAUTHORIZED,
                                   HTTP_400_BAD_REQUEST)
from posts_app.models import Comment
from posts_app.tests.utils import (create_original_comment, create_post,
                                   create_sub, create_user)

import json

class TestEditChildComment(APITestCase):
    
    def setUp(self):
        
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)
        self.original_comment = create_original_comment(self.post, self.sub)
        self.child_comment = Comment.objects.create(
            owner=self.sub,
            commentfeed=self.original_comment.commentfeed,
            text='this is the comment to edit',
            has_parent=False,
            is_original=False,
            parent_comment=None
        )
        
        self.path = '/api/v1/posts/edit-child-comment/%s/' %(str(self.child_comment.uuid))
        self.data = json.dumps({
            'text': 'this is the edited comment'
        })
        self.data_type = 'application/json'
        self.client = APIClient()
    
    def test_success_response(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(path=self.path,
                                   data=self.data,
                                   content_type=self.data_type)
        status_code = HTTP_200_OK
        self.assertEqual(response.status_code, status_code)
        
        comment = Comment.objects.last()
        decoded_data = json.loads(self.data)
        self.assertEqual(comment.text, decoded_data.get('text'))
    
    def test_error_from_permission(self):
        response = self.client.put(path=self.path,
                                   data=self.data,
                                   content_type=self.data_type)
        status_code = HTTP_401_UNAUTHORIZED
        self.assertEqual(response.status_code, status_code)
    
    def test_error_from_bad_data(self):
        self.client.force_authenticate(self.user)
        bad_data = json.dumps({
            'text': None,
        })
        
        response = self.client.put(path=self.path,
                                   data=bad_data,
                                   content_type=self.data_type)
        
        status_code = HTTP_400_BAD_REQUEST
        expected_data = {
            'message': 'invalid data'
        }
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data, expected_data)
    
    def test_error_from_invalid_data(self):
        self.client.force_authenticate(self.user)
        invalid_data = json.dumps({
            'this is not supposed to work': 'test'
        })
        response = self.client.put(path=self.path,
                                   data=invalid_data,
                                   content_type=self.data_type)
        
        status_code = HTTP_400_BAD_REQUEST
        expected_data = {
            'message': 'invalid data'
        }
        
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.data, expected_data)