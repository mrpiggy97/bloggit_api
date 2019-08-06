#test for CommentFeedSerializer

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from posts_app.models import Post, CommentFeed, Comment
from posts_app.serializers.CommentFeedSerializer import CommentFeedSerializer
from posts_app.serializers.CommentSerializer import CommentSerializer

from users_app.models import Sub


user_test_data = {
    'username': 'newusertesting10',
    'password': 'password332343',
    'email': 'testinguser@test.com'
}

class TestCommentFeedSerializer(APITestCase):
    '''test for CommentFeedSerializer model'''

    def setUp(self):
        #create a bunch of comment mainly for the read test

        self.serializer = CommentFeedSerializer

        self.user = User.objects.create_user(**user_test_data)

        self.sub = Sub.objects.create(user=self.user)

        self.post = Post.objects.create(
            title="testing commentfeed serializer",
            text="testing commentfeed serialier",
            owner=self.sub
        )

        self.post.communities.add("test")

        self.commentfeed = CommentFeed.objects.create(post=self.post)

        self.original_comment = Comment.objects.create(
            text="this is a comment",
            owner=self.sub,
            commentfeed=self.commentfeed
        )

        self.comment2 = Comment.objects.create(
            text="this is another comment",
            owner=self.sub,
            commentfeed=self.commentfeed,
            is_original=False
        )

        self.comment3 = Comment.objects.create(
            text="this is another comment",
            owner=self.sub,
            commentfeed=self.commentfeed,
            is_original=False
        )

        self.comment4 = Comment.objects.create(
            text="this is another comment",
            owner=self.sub,
            commentfeed=self.commentfeed,
            is_original=False
        )

        self.comment5 = Comment.objects.create(
            text="this is another comment",
            owner=self.sub,
            commentfeed=self.commentfeed,
            parent_comment=self.comment4,
            is_original=False,
            has_parent=True
        )
    
    def test_read_commentfeed(self):
        #test data from serializer is as expected and it works

        original_comment = self.commentfeed.get_original_comment
        children_comments = self.commentfeed.get_children_comments

        expected_data = {
            'uuid': str(self.commentfeed.uuid),
            'original_comment': CommentSerializer(original_comment).data,
            'children_comments': CommentSerializer(children_comments, many=True).data,
        }

        serializer = self.serializer(self.commentfeed)

        self.assertEqual(expected_data,  serializer.data)
    
    def test_create_commentfeed(self):
        data = {
            'post_uuid': str(self.post.uuid)
        }

        serializer = self.serializer()
        self.assertIsInstance(serializer.create(data), CommentFeed)
    
    def test_update_commentfeed(self):
        #this serializer does not update the instance as
        #updating a commentfeed instance serves no purpose

        #create a new post and assume well try to change the commentfeed's
        #post

        new_post = Post.objects.create(
            title="new post",
            text="new post test",
            owner=self.sub,
        )

        new_post.communities.add("test")

        data = {
            'post_uuid': str(new_post.uuid)
        }

        serializer = self.serializer(self.commentfeed)

        self.assertIsNone(serializer.update(self.commentfeed, data))