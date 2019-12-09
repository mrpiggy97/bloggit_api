#test PostSerializer

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from posts_app.models import Post
from posts_app.serializers.PostSerializer import PostSerializer

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

        self.user = User.objects.create_user(**user_test_data)

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
            'user_id': self.user.id,
            'add_communities': ['testing', 'test'],
            'title': 'this is the title',
            'text': 'this is the text',
        }

        serializer = self.serializer(data=data)

        self.assertTrue(serializer.is_valid())
    
    def test_create_post(self):
        #this data is supposed to reprent validated_data in serializer
        #create method now we are testing if update method will return a post
        #object, remove_communities doesn't need to be provided but becasuse
        #we are testing update method directly we need to pass it
        data = {
            'user_id': self.user.id,
            'title': 'this is a title',
            'text': 'this is the text',
            'add_communities': ['title', 'test', 'third tag'],
            'remove_communities': None
        }

        context = {'session_sub': self.sub}

        serializer = self.serializer()

        self.assertIsInstance(serializer.create(data), Post)
    
    def test_update_post(self):
        #this block is attempting to create a post successfuly

        #this data is expected to work, it is supposed to represent validated
        #data
        data = {
            'user_id': self.post.owner.user.id,
            'title': 'changed title',
            'text': 'changed text',
            'add_communities': None,
            'remove_communities': ['test']
        }

        serializer = self.serializer(self.post)

        self.assertIsInstance(serializer.update(self.post, data), Post)
    
    def test_create_error_from_non_existing_user(self):
        '''if no user in the app can get retrieved through'''
        '''user_id then the serializer should throw an Execption'''
        data = {
            'title': 'this is the title',
            'text': 'this is the text',
            'add_communities': ['text'],
            'user_id': 1000,
        }
        
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            self.assertRaises(Exception,
                              serializer.save)
        
        #no object should've been created so the count has to remain as 1
        self.assertEqual(Post.objects.count(), 1)
    
    def test_create_error_from_non_existing_sub(self):
        '''if for any reason no sub was created when a user has'''
        '''the serializer then has to raise an expection as well'''
        '''this is unlikely to happen since endpoint register_v1'''
        '''specifically addresses this'''
        
        new_user = User.objects.create_user(
            username='thisisntasda',
            email='nodded@emailfake.com',
            password='1343lskldfkop23'
        )
        
        data = {
            'title': 'this is the new title',
            'text': 'this is the text',
            'add_communities': ['test'],
            'user_id': new_user.id
        }
        
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            self.assertRaises(Exception, serializer.save)
    
    def test_error_from_non_owner_trying_update(self):
        new_user = User.objects.create_user(
            username='thisisnqdad2432',
            email='testingemail@test.com',
            password='thisalkssld234'
        )
        new_sub = Sub.objects.create(user=new_user)
        data = {
            'title': 'this is the title',
            'text': 'this is the text',
            'user_id': new_user.id,
            'add_communities': ['test']
        }
        serializer = self.serializer(self.post, data=data)
        
        if serializer.is_valid():
            self.assertRaises(Exception, serializer.save)