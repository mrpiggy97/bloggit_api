#test creation, updating and expected data from
#ChildCommentSerializer

from rest_framework.test import APITestCase

from posts_app.models import Comment, CommentFeed
from posts_app.serializers.CommentSerializer import ChildCommentSerializer
from posts_app.tests.utils import (create_original_comment, create_post,
                                   create_sub, create_user)

class TestChildCommentSerializer(APITestCase):
    
    def setUp(self):
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)
        self.first_comment = create_original_comment(self.post, self.sub)
        self.commentfeed = CommentFeed.objects.first()
        self.child_comment = Comment.objects.create(text="text",
                                                    owner=self.sub,
                                                    commentfeed=self.commentfeed,
                                                    is_original=False)
        
        self.serializer = ChildCommentSerializer
    
    def test_expected_data(self):
        expected_data = {
            'uuid': self.child_comment.get_uuid_as_string,
            'liked': None,
            'reported': None,
            'date': self.child_comment.get_date_posted,
            'parent_comment': self.child_comment.get_parent_comment,
            'pic': self.child_comment.get_pic,
            'owner': self.child_comment.get_owner_info,
            'is_original': False,
            'has_parent': False,
            'likes': self.child_comment.likes,
            'reports': self.child_comment.reports,
            'text': self.child_comment.text
        }
        
        serializer_data = self.serializer(self.child_comment, context=None).data
        self.assertEqual(expected_data, serializer_data)
    
    def test_is_valid_and_create_without_parent(self):
        data = {
            'text': 'this is a new comment',
            'owner_uuid': str(self.sub.uuid),
            'commentfeed_uuid': str(self.commentfeed.uuid)
        }
        
        serializer = self.serializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        if serializer.is_valid():
            serializer.save()
        
        self.assertEqual(Comment.objects.count(), 3)
        
        last_comment = Comment.objects.last()
        
        self.assertFalse(last_comment.is_original)
        self.assertFalse(last_comment.has_parent)
    
    def test_is_valid_and_create_with_parent(self):
        new_comment = Comment.objects.create(
            text='this  will be the new parent comment',
            owner=self.sub,
            commentfeed=self.commentfeed,
        )
        data = {
            'text': 'this comment will be a child',
            'commentfeed_uuid': str(self.commentfeed.uuid),
            'owner_uuid': str(self.sub.uuid),
            'parent_uuid': str(new_comment.uuid),
        }
        
        serializer = self.serializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        if serializer.is_valid():
            serializer.save()
        
        last_comment = Comment.objects.last()
        self.assertTrue(last_comment.has_parent)
    
    
    def test_update(self):
        data = {
            'text': 'this is the new text'
        }
        
        bad_data = {
            'text': 'this is not supposed to work',
            'owner_uuid': str(self.sub.uuid)
        }
        
        new_comment = Comment.objects.create(
            text='this is the text for the child comment',
            owner=self.sub,
            commentfeed=self.commentfeed,
            is_original=False
        )
        
        serializer = self.serializer(new_comment, data=data)
        serializer2 = self.serializer(new_comment, data=bad_data)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer2.is_valid())
        
        if serializer.is_valid():
            serializer.save()
        
        comment = Comment.objects.last()
        self.assertEqual(data['text'], comment.text)
        
        self.assertRaises(Exception, serializer2.update, new_comment, bad_data)