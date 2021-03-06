#test report-post endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.tests.utils import create_post, create_sub, create_user
from posts_app.models import Post

from users_app.models import Sub

class TestReportPost(APITestCase):
    
    def setUp(self):
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)
        
        self.path = '/api/v1/users/report-post/{0}/'.format(str(self.post.uuid))
        self.client = APIClient()
    
    def test_success_response(self):
        
        self.client.force_authenticate(self.user)
        response = self.client.put(path=self.path)
        
        post = Post.objects.first()
        sub = Sub.objects.first()
        reported_posts = sub.reported_posts_as_list
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.reports, 1)
        self.assertTrue(str(post.uuid) in reported_posts)
    
    def test_response_from_unauthenticated_request(self):
        response = self.client.put(path=self.path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unnessesary_request(self):
        sub = Sub.objects.first()
        reported_posts = sub.reported_posts_as_list
        reported_posts.append(str(self.post.uuid))
        sub.reported_posts_as_list = reported_posts
        self.client.force_authenticate(self.user)
        
        response = self.client.put(path=self.path)
        
        #response should be a status code of 501 because
        #post uuid is already in sub.reported_posts
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)