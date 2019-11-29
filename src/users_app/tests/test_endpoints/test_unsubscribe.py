from rest_framework.test import APIClient, APITestCase
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED

from posts_app.tests.utils import create_user, create_sub

from users_app.models import Sub

from taggit.models import Tag

class TestUnsubscribe(APITestCase):
    
    def setUp(self):
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.community = Tag.objects.create(name='test')
        self.sub.communities.add(self.community.slug)
        
        self.path = '/api/v1/users/unsubscribe/%s/' %(self.community.slug)
        self.client = APIClient()
    
    def test_success_response(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(data=None, path=self.path)
        self.assertEqual(response.status_code, HTTP_202_ACCEPTED)
        
        sub = Sub.objects.first()
        self.assertTrue(sub.get_communities_as_list == [])
    
    def test_error_response_from_permission(self):
        
        response = self.client.delete(data=None, path=self.path)
        sub = Sub.objects.first()
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        self.assertEqual(sub.get_communities_as_list, [self.community.slug])