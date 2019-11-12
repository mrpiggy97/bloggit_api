#test get-comment endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.models import Post, Comment, CommentFeed
from posts_app.serializers.CommentSerializer import (OriginalCommentSerializer,
                                                     ChildCommentSerializer)
from posts_app.tests.utils import (create_original_comment, create_post,
                                   create_sub, create_user)

class TestGetComment(APITestCase):
    
    def setUp(self):
        
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)
        self.original_comment = create_original_comment(self.post, self.sub)
        self.commentfeed = CommentFeed.objects.first()
        self.child_comment = Comment.objects.create(
            owner=self.sub,
            text='child comment',
            commentfeed=self.commentfeed,
            is_original=False
        )
        self.original_comment_serializer = OriginalCommentSerializer
        self.child_serializer = ChildCommentSerializer
        
        self.client = APIClient()
        self.path = '/posts/get-comment/%s/' %(str(self.original_comment.uuid))
        self.path2 = '/posts/get-comment/%s/' %(str(self.child_comment.uuid))
        
    def test_get_original_comment(self):
        
        context = {'session_sub': self.sub}
        
        comment_data1 = self.original_comment_serializer(self.original_comment,
                                                   context=None).data
        comment_data2 = self.original_comment_serializer(self.original_comment,
                                                   context=context).data
        
        expected_data1 = {
            'authenticated': False,
            'comment': comment_data1
        }
        
        expected_data2 = {
            'authenticated': True,
            'comment': comment_data2
        }
        
        response1 = self.client.get(path=self.path)
        self.client.force_authenticate(self.user)
        response2 = self.client.get(path=self.path)
        self.assertEqual(expected_data1, response1.data)
        self.assertEqual(expected_data2, response2.data)
        
        code = status.HTTP_200_OK
        self.assertEqual(response1.status_code, code)
        self.assertEqual(response2.status_code, code)
    
    def test_get_child_comment(self):
        
        context = {'session_sub': self.sub}
        
        comment_data1 = self.child_serializer(self.child_comment,
                                               context=None).data
        comment_data2 = self.child_serializer(self.child_comment,
                                               context=context).data
        
        expected_data1 = {
            'authenticated': False,
            'comment': comment_data1
        }
        
        expected_data2 = {
            'authenticated': True,
            'comment': comment_data2
        }
        
        
        code = status.HTTP_200_OK
        
        response1 = self.client.get(path=self.path2)
        
        self.client.force_authenticate(self.user)
        response2 = self.client.get(path=self.path2)
        
        self.assertEqual(response1.data, expected_data1)
        self.assertEqual(response2.data, expected_data2)
        
        self.assertEqual(response1.status_code, code)
        self.assertEqual(response2.status_code, code)