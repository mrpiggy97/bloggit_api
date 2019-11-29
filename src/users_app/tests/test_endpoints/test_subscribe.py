from rest_framework.test import APIClient, APITestCase
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED

from posts_app.tests.utils import create_sub, create_user

from users_app.models import Sub

from taggit.models import Tag

class TestSubscribe(APITestCase):
    
    def setUp(self):
    
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.community = Tag.objects.create(name='first community')
        
        self.client = APIClient()
        self.path = '/api/v1/users/subscribe/%s/' %(self.community.slug)
    
    def test_success_response(self):
        self.client.force_authenticate(self.user)
        response = self.client.put(data=None, path=self.path)
        sub = Sub.objects.first()
        self.assertEqual(response.status_code, HTTP_202_ACCEPTED)
        self.assertTrue(self.community.slug in sub.get_communities_as_list)
    
    def test_error_response_from_permission(self):
        response = self.client.put(data=None, path=self.path)
        sub = Sub.objects.first()
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(sub.get_communities_as_list, [])