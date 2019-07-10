#test endpoints for posts_app

from django.contrib.auth.models import User

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.models import Post
from posts_app.serializers.PostSerializer import PostSerializer

from users_app.models import Sub

from taggit.models import Tag

import json

user_test_data = {
    'username': 'newusertesting23',
    'password': 'ldkkasl2334',
    'email': 'newemail@email.com'
    }
    
def create_user():
    return User.objects.create_user(**user_test_data)

def create_sub(user):
    return Sub.objects.create(user=user)

def create_post(owner):
    return Post.objects.create(
        title='this is the title',
        text='this is a test',
        owner=owner
    )

#each class is a test for a determined endpoint, no class should be
#inherited from other class to extend test functionality

class TestGetPost(APITestCase):
    '''test endpoint get-post/post_uuid/'''

    def setUp(self):

        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)

        self.path = '/posts/get-post/%s/' %(str(self.post.uuid))

        self.client = APIClient()
    
    def test_response(self):
        
        response = self.client.get(path=self.path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_wrong_method_response(self):
        '''test what would happen if we made a request'''
        '''to self.path with the wrong method'''

        response = self.client.post(path=self.path)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestEditPost(APITestCase):
    '''test edit-post endpoint'''

    def setUp(self):
        
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)

        self.path = '/posts/edit-post/%s/' %(str(self.post.uuid))
        self.client = APIClient()
        self.data = json.dumps({
            'title': 'edited title',
            'text': 'edited text',
            'owner_uuid': str(self.post.owner.uuid)
        })
    
    def test_success_response(self):

        self.client.force_authenticate(self.user)
        response = self.client.put(path=self.path, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_error_response(self):
        '''test if we are granted permission if a'''
        '''user other than post.owner tries to edit the post'''

        #first we have to create a new user and a new sub
        #sub because PostView make a query to get the sub belonging
        #to that new user, there should always be a sub per user
        new_user = User.objects.create_user(
            username='otheruserqwe',
            password='newpassword47',
            email='newemail@mail.com'
        )

        #now authenticate that new user
        self.client.force_authenticate(user=new_user)

        #make call
        response = self.client.put(path=self.path, data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_error_response_from_bad_data(self):
        #test http response given when serializer is not valid

        bad_data = json.dumps({
            'title': 'new tle',
            'text': 'new text',
            'owner_uuid': None
        })

        self.client.force_authenticate(user=self.post.owner.user)
        response = self.client.put(path=self.path, data=bad_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_304_NOT_MODIFIED)


class TestMakePost(APITestCase):
    '''testing make-post endpoint'''

    def setUp(self):

        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)

        self.path = '/posts/make-post/'
        self.client = APIClient()
        self.data = json.dumps({
            'title': 'this is a new post',
            'text': 'this is a new post',
            'owner_uuid': str(self.sub.uuid),
            'add_communities': ['test', 'first post']
        })
    
    def test_successful_creation(self):
        #this is how a call should be valid
        self.client.force_authenticate(user=self.sub.user)
        response = self.client.post(path=self.path, data=self.data, format='json')

        #we will test response status code and if indeed a post has been created

        post = Post.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.title, 'this is a new post')
    
    def test_error_response_from_permission(self):

        response = self.client.post(path=self.path, data=self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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


class TestPostsByCommunity(APITestCase):
    '''test posts-by-community endpoint'''

    def setUp(self):

        #first create a user a sub and a couple of posts

        self.user = User.objects.create(**user_test_data)
        self.sub = Sub.objects.create(user=self.user)

        for n in range (0, 4):
            Post.objects.create(
                title='new post',
                text='new post',
                owner=self.sub
            )
        
        for post in Post.objects.all():
            post.communities.add('test')
        
        self.path = '/posts/posts-by-community/%s/' %('test')
        self.client = APIClient()
        self.slug = 'test'
        self.serializer = PostSerializer

    def test_success_response(self):
        #this request should be successful and return a 200 ok http response
        #along with a list of posts related to a community(tag)
        response = self.client.get(path=self.path)

        community = Tag.objects.first()
        posts = Post.objects.filter(communities=community).order_by('-id')[0:250]
        posts_data = self.serializer(posts, context=None, many=True).data
        test_data = json.dumps({
            'posts': posts_data,
            'subscribed': None
        })
        self.assertEqual(response.data, test_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)