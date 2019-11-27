from rest_framework.test import APIClient, APITestCase
from rest_framework.status import HTTP_200_OK

from posts_app.models import CommentFeed
from posts_app.tests.utils import (create_original_comment, create_post,
                                   create_sub, create_user, create_child_comment)

class TestSubComments(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)
        
        for n in range(0, 11):
            create_original_comment(self.post, self.sub)
        
        commentfeed = CommentFeed.objects.first()
        for n in range(0, 11):
            create_child_comment(commentfeed, self.sub)
        
        self.client = APIClient()
        self.path = '/api/v1/users/sub-comments/%s/?page=1' %(str(self.sub.uuid))
    
    def test_success_response(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, HTTP_200_OK)