#test edit_post endpoint

from django.contrib.auth.models import User

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.models import Post
from posts_app.serializers import PostSerializer

from users_app.models import Sub

import json

class TestEditPost(APITestCase):
    '''test endpoint to edit posts'''

    def setUp(self):

        self.user = User.objects.create_user(
            username='testingusername12',
            password='testingpassword22',
            email='testingemail@test.com'
        )

        self.sub = Sub.objects.create(user=self.user)

        self.post = Post.objects.create(
            title='this is the title',
            text='tjis is the text',
            owner=self.sub
        )

        self.post.communities.add('test')

        self.serializer = PostSerializer

        self.path = '/posts/edit-post/%s/' %(str(self.post.uuid))

        self.client = APIClient()
    
    def test_success_request(self):
        test_data = json.dumps({
            'title': 'updated test',
            'text': 'updated text',
            'owner_uuid': str(self.post.owner.uuid)
        })

        self.client.force_authenticate(user=self.user)

        response = self.client.put(path=self.path, data=test_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)