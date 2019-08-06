#test delete-post endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.tests.utils import create_post, create_sub, create_user


class TestDeletePost(APITestCase):
    '''test delete-post endpoint'''

    def setUp(self):

        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)

        self.path = '/posts/delete-post/%s/' %(str(self.post.uuid))
        self.client = APIClient()
    
    def test_success_response(self):

        self.client.force_authenticate(user=self.post.owner.user)
        response = self.client.delete(path=self.path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)