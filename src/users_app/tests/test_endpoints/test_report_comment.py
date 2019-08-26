#test report-comment endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.tests.utils import (create_original_comment, create_post,
                                   create_sub, create_user)
from posts_app.models import Comment

from users_app.models import Sub


class TestReportComment(APITestCase):
    
    def setUp(self):
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)
        self.comment = create_original_comment(self.post, self.sub)
        
        self.path = '/users/report-comment/{0}/'.format(str(self.comment.uuid))
        self.client = APIClient()
    
    def test_success_response(self):
        
        self.client.force_authenticate(self.user)
        
        response = self.client.put(path=self.path)
        comment = Comment.objects.first()
        sub = Sub.objects.first()
        reported_comments = sub.reported_comments_as_list
        
        self.assertEqual(comment.reports, 1)
        self.assertTrue(str(comment.uuid) in reported_comments)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_response_from_unauthenticated_request(self):
        response = self.client.put(path=self.path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unnessesary_request(self):
        sub = Sub.objects.first()
        reported_comments = sub.reported_comments_as_list
        reported_comments.append(str(self.comment.uuid))
        sub.reported_comments_as_list = reported_comments
        self.client.force_authenticate(self.user)
        
        response = self.client.put(path=self.path)
        #response should be a status code of 501 since comment uuid
        #is already in sub.reported_comments
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)