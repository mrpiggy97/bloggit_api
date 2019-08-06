#test for CommentSerializer

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from posts_app.models import Post, CommentFeed, Comment
from posts_app.serializers.CommentSerializer import CommentSerializer

from users_app.models import Sub

user_test_data = {
    'username': 'newusertesting10',
    'password': 'password332343',
    'email': 'testinguser@test.com'
}


class TestCommentSerializer(APITestCase):
    '''test read create update in CommentSerializer'''
    '''and check that data passed to serialier is valid'''

    def setUp(self):

        self.user = User.objects.create_user(**user_test_data)

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
    

    def test_valid_data(self):
        #test if data if valid

        data = {
            'owner_uuid': str(self.comment.owner.uuid),
            'commentfeed_uuid': str(self.comment.commentfeed.uuid),
            'text': 'this is a text',
        }

        serializer = self.serializer(data=data)

        self.assertTrue(serializer.is_valid())
    
    def test_create_comment(self):
        #check that create method works as expected

        data = {
            'text': 'this is a comment test',
            'owner_uuid': str(self.sub.uuid),
            'commentfeed_uuid': str(self.commentfeed.uuid),
        }

        serializer = self.serializer()

        self.assertIsInstance(serializer.create(data), Comment)
    

    def test_update_comment(self):

        #likes and reports are optional fields providing them is not nessesary
        #has_parent and is_original fields don't do anything when updating
        #providing them is not nessesary

        #to test that serializer can't change a comment's commentfeed
        new_commentfeed = CommentFeed.objects.create(post=self.post)

        data = {
            'text': 'updated comment text',
            'likes': 100,
            'reports': 100,
            'owner_uuid': str(self.comment.owner.uuid),
            'commentfeed_uuid': str(self.commentfeed.uuid)
        }

        wrong_data = {
            'text': 'edit',
            'likes': 22,
            'reports': 42,
            'owner_uuid': str(self.comment.owner.uuid),
            'commentfeed_uuid': str(new_commentfeed.uuid)
        }

        serializer = self.serializer(self.comment)

        #this one should not work
        serializer2 = self.serializer(self.comment)

        self.assertIsInstance(serializer.update(self.comment, data), Comment)
        self.assertIsNone(serializer2.update(self.comment, wrong_data))