#test like-post endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.models import Post
from posts_app.tests.utils import create_post, create_sub, create_user

from users_app.models import Sub

class TestLikePost(APITestCase):
    
    def setUp(self):
        
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)
        
        self.path = '/api/v1/users/like-post/{0}/'.format(str(self.post.uuid))
        self.client = APIClient()
    
    def test_success_response(self):
        
        self.client.force_authenticate(user=self.user)
        response = self.client.put(path=self.path)
        
        post = Post.objects.first()
        session_sub = Sub.objects.first()
        liked_posts = session_sub.liked_posts_as_list
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.likes, 2)
        self.assertTrue(str(post.uuid) in liked_posts)
    
    def test_response_from_unauthenticated_request(self):
        response = self.client.put(path=self.path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_unnessesary_request(self):
        sub = Sub.objects.first()
        liked_posts = sub.liked_posts_as_list
        liked_posts.append(str(self.post.uuid))
        sub.liked_posts_as_list = liked_posts
        self.client.force_authenticate(self.user)
        
        response = self.client.put(path=self.path)
        #since post uuid in already in sub.liked_posts response
        #should be a 501 http status code
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)