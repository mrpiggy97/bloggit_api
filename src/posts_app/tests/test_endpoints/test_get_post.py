from django.contrib.auth.models import User

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.models import Post

from users_app.models import Sub

class TestGetPost(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="testinguser24",
            password="passwrod34",
            email="testingemail@mail.com"
        )

        self.sub = Sub.objects.create(user=self.user)

        self.post = Post.objects.create(
            title="testing endpoint",
            text="testing endpoint",
            owner=self.sub,
        )

        self.post.communities.add("test")

        self.client = APIClient()
        self.path = '/posts/get-post/%s/' %(str(self.post.uuid))
    
    def test_success(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)