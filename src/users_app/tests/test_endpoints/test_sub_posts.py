from rest_framework.test import APIClient, APITestCase
from rest_framework.status import HTTP_200_OK

from posts_app.tests.utils import (create_user, create_sub,
                                   create_post, create_original_comment)

from users_app.models import Sub

class TestSubPosts(APITestCase):
    
    def setUp(self):
        self.user = create_user()
        self.sub = create_sub(self.user)
        
        for n in range(0, 21):
            create_post(self.sub)
        
        self.path = '/api/v1/users/sub-posts/%s/?page=2' %(str(self.sub.uuid))
        self.client = APIClient()
        
    
    def test_success_response(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, HTTP_200_OK)