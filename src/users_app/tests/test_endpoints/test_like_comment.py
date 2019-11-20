#test like-comment endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.models import Comment
from posts_app.tests.utils import (create_post, create_sub,
                                   create_user, create_original_comment)

from users_app.models import Sub

class TestLikeComment(APITestCase):
    
    def setUp(self):
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)
        self.comment = create_original_comment(self.post, self.sub)
        
        self.path = '/api/v1/users/like-comment/{0}/'.format(str(self.comment.uuid))
        self.client = APIClient()
    
    def test_success_response(self):
        self.client.force_authenticate(self.user)
        
        response = self.client.put(path=self.path)
        comment = Comment.objects.first()
        sub = Sub.objects.first()
        liked_comments = sub.liked_comments_as_list
        
        self.assertEqual(comment.likes, 2)
        self.assertTrue(str(comment.uuid) in liked_comments)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_response_from_unauthenticated_request(self):
        response = self.client.put(path=self.path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unnessesary_request(self):
        sub = Sub.objects.first()
        liked_comments = sub.liked_comments_as_list
        liked_comments.append(str(self.comment.uuid))
        sub.liked_comments_as_list = liked_comments
        self.client.force_authenticate(self.user)
        
        response = self.client.put(path=self.path)
        
        #response should return a 501 http status code
        #since uuid is already in sub.liked_comments encoded list
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)