#test serializers for posts_app

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from posts_app.models import Post, CommentFeed, Comment
from posts_app.serializers import PostSerializer, CommentSerializer

from users_app.models import Sub

user_test_data = {
    'username': 'newusertesting10',
    'password': 'password332343',
    'email': 'testinguser@test.com'
}

class TestPostSerializer(APITestCase):
    '''test create read and update methods'''

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
    
    def test_create_post(self):
        data = {
            'owner_uuid': str(self.sub.uuid),
            'title': 'this is a title',
            'text': 'this is the text',
            'add_communities': ['title', 'test', 'third tag'],
        }

        context = {'session_sub': self.sub}

        serializer = self.serializer(data=data, context=context)

        #first test if serializer is valid as expected
        self.assertTrue(serializer.is_valid())

        if serializer.is_valid():
            serializer.save()
        
        test_post = Post.objects.last()
        test_serializer = self.serializer(test_post, context=context)

        #test if serializer from last post created is
        #the same as the one that was hopefully created
        self.assertEqual(serializer.data, test_serializer.data)

        #check that uuid is a string
        self.assertEqual(str(test_post.uuid), test_serializer.data['uuid'])
    
    def test_update_post_with_correct_data(self):
        #this block is attempting to create a post successfuly

        #this data is expected to work
        data = {
            'owner_uuid': str(self.post.owner.uuid),
            'title': 'changed title',
            'text': 'changed text'
        }

        context = {'session_sub': self.sub}

        serializer = self.serializer(self.post, data=data, context=context)
        self.assertTrue(serializer.is_valid())

        test_post = Post.objects.first()
        test_serializer = self.serializer(test_post, context=context)

        self.assertEqual(test_serializer.data, serializer.data)

    def test_udpate_with_wrong_data(self):

        #this will try to update self.post with a different owner

        #first create a new user
        new_user = User.objects.create(
            username="usercan'tupdatepost30",
            password="thisisthepassword22",
            email="newemail@mail.com"
        )

        new_sub = Sub.objects.create(user=new_user)

        should_not_work = {
            'owner_uuid': str(new_sub.uuid),
            'title': 'should not work',
            'text': 'should not work',
        }

        serializer = self.serializer(self.post)

        #check that update method does not return an instance object
        self.assertIsNone(serializer.update(self.post, should_not_work))


class TestCommentSerializer(APITestCase):
    '''test read create and update for CommentSerializer'''

    def setUp(self):

        self.user = User.objects.create_user(
            username=user_test_data['username'],
            password=user_test_data['password'],
            email=user_test_data['email']   
        )

        self.sub = Sub.objects.create(user=self.user)

        self.post = Post.objects.create(
            title="testing comment",
            text="testing comment serializer",
            owner=self.sub
        )
        self.post.communities.add("test")

        self.commentfeed = CommentFeed.objects.create(post=self.post)

        self.comment = Comment.objects.create(
            text='this is the first comment',
            owner=self.sub,
            commentfeed=self.commentfeed
        )

        self.serializer = CommentSerializer
    
    def test_read_comment(self):
        #check that data recieved from serializer is exactly as expeted
        expected_data = {
            'owner': self.comment.get_owner_info,
            'text': self.comment.text,
            'uuid': self.comment.get_uuid_as_string,
            'date': self.comment.get_date_posted,
            'is_original': True,
            'has_parent': False,
            'pic': None,
            'parent_comment': None,
            'likes': self.comment.likes,
            'reports': self.comment.reports,
            'liked': None,
            'reported': None
        }

        serializer = self.serializer(self.comment)

        self.assertEqual(serializer.data, expected_data)
    
    def test_create_comment(self):
        data = {
            'text': 'this is a comment test',
            'owner_uuid': str(self.sub.uuid),
            'commentfeed_uuid': str(self.commentfeed.uuid),
        }

        serializer = self.serializer(data=data)

        #first check if serializer is valid as how it is
        self.assertTrue(serializer.is_valid())

        if serializer.is_valid():
            serializer.save()
        
        test_comment = Comment.objects.last()
        test_serializer = CommentSerializer(test_comment)

        self.assertEqual(test_serializer.data, serializer.data)
    

    def test_update_comment_with_correct_data(self):

        #likes and reports are optional fields providing them is not nessesary
        #has_parent and is_original fields don't do anything when updating
        #providing them is not nessesary
        expected_data = {
            'text': 'updated comment text',
            'likes': 100,
            'reports': 100,
            'owner_uuid': str(self.comment.owner.uuid),
            'commentfeed_uuid': str(self.commentfeed.uuid)
        }

        serializer = self.serializer(self.comment, data=expected_data)
        self.assertTrue(serializer.is_valid())

        if serializer.is_valid():
            serializer.save()

        test_comment = Comment.objects.first()
        test_serializer = CommentSerializer(test_comment)

        self.assertEqual(test_serializer.data, serializer.data)
        self.assertEqual(test_comment.likes, 100)
    
    def test_update_with_wrong_data(self):
        #create a new commentfeed (or a sub it doesn't matter) and try to
        #use it uuid to update the comment, this should not work

        new_commentfeed = CommentFeed.objects.create(post=self.post)

        should_not_work = {
            'text': 'should not work',
            'owner_uuid': str(self.sub.uuid),
            'commentfeed_uuid': str(new_commentfeed.uuid),
            'likes': 33 #not necessary to include
        }

        serializer = self.serializer(self.comment)

        #commentfeed_uuid is not the same as the objects original
        #commentfeed.uuid so .update() should return None
        self.assertIsNone(serializer.update(self.comment, should_not_work))