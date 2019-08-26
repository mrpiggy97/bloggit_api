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
        
        self.path = '/users/like-post/{0}/'.format(str(self.post.uuid))
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