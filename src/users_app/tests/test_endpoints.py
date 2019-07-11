#test endpoints in users_app

from django.contrib.auth.models import User

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from posts_app.models import Post, Comment, CommentFeed
from posts_app.serializers.PostSerializer import PostSerializer
from posts_app.serializers.CommentSerializer import CommentSerializer

from users_app.models import Sub

import json

user_test_data = {
    'username': 'newuser1234',
    'password': 'password12345',
}

def create_user():
    return User.objects.create_user(**user_test_data)

def create_sub(user):
    return Sub.objects.create(user=user)

def create_post(sub):
    new_post = Post.objects.create(
        title='this is a new post',
        text='this is a new post',
        owner=sub
        )
    new_post.communities.add('post')
    return new_post

def create_commentfeed(post):
    return CommentFeed.objects.create(post=post)

def create_comment(commentfeed, sub):
    return Comment.objects.create(
        text='this is a comment',
        owner=sub,
        commentfeed=commentfeed
    )

class TestProfile(APITestCase):
    '''test endpoint profile/<uuid>/'''

    def setUp(self):
        #we need to create posts, commentfeeds, comments a sub, a user
        #then we will go on with the test

        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post1 = create_post(self.sub)
        self.post2 = create_post(self.sub)
        self.post3 = create_post(self.sub)
        self.post4 = create_post(self.sub)

        self.commentfeed = create_commentfeed(self.post1)
        self.commentfeed2 = create_commentfeed(self.post2)

        self.comment1 = create_comment(self.commentfeed, self.sub)
        self.comment2 = create_comment(self.commentfeed, self.sub)
        self.comment3 = create_comment(self.commentfeed2, self.sub)
        self.comment4 = create_comment(self.commentfeed2, self.sub)

        self.path = '/users/profile/%s/' %(str(self.sub.uuid))

        self.client = APIClient()
    
    def test_success_response(self):

        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)