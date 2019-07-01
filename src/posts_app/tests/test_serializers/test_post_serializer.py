#test PostSerializer

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from posts_app.models import Post
from posts_app.serializers import PostSerializer

from users_app.models import Sub

user_test_data = {
    'username': 'newusertesting10',
    'password': 'password332343',
    'email': 'testinguser@test.com'
}


class TestPostSerializer(APITestCase):
    '''test create read, update methods and '''
    '''if data provided to serializer will be valid'''
    def setUp(self):
        self.user = User.objects.create_user(
            username=user_test_data['username'],
            password=user_test_data['password'],
            email=user_test_data['email']
        )

        self.sub = Sub.objects.create(user=self.user)

        self.post = Post.objects.create(
            owner=self.sub,
            title="this is the title",
            text="this is the text"
        )

        self.post.communities.add("test")

        self.serializer = PostSerializer

    def test_read_post(self):
        #first a post with its data serialized needs
        #to be created

        new_post = Post.objects.create(
            title="this is the post to read",
            text="this is the post to read",
            owner=self.sub
        )

        new_post.communities.add("test")

        serializer = self.serializer(new_post)

        #data from serializer should be equal to this
        expected_data = {
            'uuid': str(new_post.uuid),
            'title': new_post.title,
            'text': new_post.text,
            'communities_list': new_post.get_communities_as_list,
            'liked': None,
            'reported': None,
            'likes': new_post.likes,
            'reports': new_post.reports,
            'owner': new_post.get_owner_info,
            'pic': new_post.get_pic,
            'date': new_post.get_date_posted
        }

        self.assertEqual(serializer.data, expected_data)
    
    def test_valid_serializer_data(self):
        #test if data passed to serializer will be valid

        data = {
            'owner_uuid': str(self.sub.uuid),
            'add_communities': ['testing', 'test'],
            'title': 'this is the title',
            'text': 'this is the text',
        }

        serializer = self.serializer(data=data)

        self.assertTrue(serializer.is_valid())
    
    def test_create_post(self):
        data = {
            'owner_uuid': str(self.sub.uuid),
            'title': 'this is a title',
            'text': 'this is the text',
            'add_communities': ['title', 'test', 'third tag'],
        }

        context = {'session_sub': self.sub}

        serializer = self.serializer()

        self.assertIsInstance(serializer.create(data), Post)
    
    def test_update_post(self):
        #this block is attempting to create a post successfuly

        #this data is expected to work
        data = {
            'owner_uuid': str(self.post.owner.uuid),
            'title': 'changed title',
            'text': 'changed text'
        }

        serializer = self.serializer(self.post)

        self.assertIsInstance(serializer.update(self.post, data), Post)

        #this block will try to change self.post.owner unsuccessfuly

        new_user = User.objects._create_user(
            username="newusertestin",
            password="newpasswoas222",
            email="newemail@email.com"
        )

        new_sub = Sub.objects.create(user=new_user)

        wrong_data = {
            'title': 'should not work',
            'text': 'should not work',
            'owner_uuid': str(new_sub.uuid)
        }

        serializer2 = self.serializer(self.post)

        self.assertIsNone(serializer2.update(self.post, wrong_data))