#test search endpoint

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.tests.utils import create_post, create_sub, create_user
from posts_app.serializers.PostSerializer import PostSerializer
from posts_app.models import Post


class TestSearch(APITestCase):
    
    def setUp(self):
        self.user = create_user()
        self.sub = create_sub(self.user)

        #create a bunch of posts some with similiar communities
        #for the response to actually return the expected filtered
        #objects
        self.post1 = create_post(self.sub)
        self.post1.communities.add('undertaker', 'wwe', 'wrestling')

        self.post2 = create_post(self.sub)
        self.post2.communities.add('undertaker', 'cm punk', 'testing')

        self.post3 = create_post(self.sub)
        self.post3.communities.add('undertaker', 'keyfabe', 'testing')

        self.post4 = create_post(self.sub)
        self.post4.communities.add('america', '4 of july')

        self.post5 = create_post(self.sub)
        self.post5.communities.add('navy', 'military')

        self.client = APIClient()
        self.path = '/posts/search/{0}/'.format('undertaker wwe')
        self.serializer = PostSerializer
    
    def test_success_response(self):
        #response should filter only self.post3 self.post2 and self.post1
        response = self.client.get(path=self.path)
        
        self.assertEqual(response.data['count'], 3)#endpoint is expected to return 3 posts
        self.assertEqual(response.status_code, status.HTTP_200_OK)