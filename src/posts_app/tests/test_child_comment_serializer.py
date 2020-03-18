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
        
        self.child_comment2 = Comment.objects.create(text="this is the second child comment",
                                                     owner=self.sub,
                                                     commentfeed=self.commentfeed,
                                                     is_original=False,
                                                     has_parent=True,
                                                     parent_comment=self.child_comment)
        
        Comment.objects.create( text="this is the text",
                                commentfeed=self.commentfeed,
                                parent_comment=self.child_comment,
                                owner=self.sub,
                                is_original=False,
                                has_parent=True)
        
        self.serializer = ChildCommentSerializer
    
    def test_expected_data(self):
        expected_data = {
            'uuid': self.child_comment.get_uuid_as_string,
            'liked': None,
            'reported': None,
            'date': self.child_comment.get_date_posted,
            'parent_comment': self.child_comment.get_parent_comment,
            'owner': self.child_comment.get_owner_info,
            'is_original': False,
            'has_parent': False,
            'likes': self.child_comment.likes,
            'reports': self.child_comment.reports,
            'text': self.child_comment.text,
            'id': self.child_comment.id
        }
        
        expected_data2 = {
            'uuid': self.child_comment2.get_uuid_as_string,
            'liked' : None,
            'reported' : None,
            'likes' : 1,
            'reports' : 0,
            'is_original' : False,
            'has_parent' : True,
            'parent_comment' : self.child_comment2.get_parent_comment,
            'date' : self.child_comment2.get_date_posted,
            'owner' : self.child_comment2.get_owner_info,
            'id' : self.child_comment2.id,
            'text' : self.child_comment2.text
        }
        
        serializer_data = self.serializer(self.child_comment, context=None).data
        serializer_data2 = self.serializer(self.child_comment2, context=None).data
        self.assertEqual(expected_data, serializer_data)
        self.assertEqual(expected_data2, serializer_data2)
    
    def test_expected_data_with_parent_comment(self):
        expected_data = {
            'owner' : self.child_comment.get_owner_info,
            'text' : self.child_comment.text,
            'uuid' : self.child_comment.get_uuid_as_string,
            'date' : self.child_comment.get_date_posted
        }
        
        serialized_comment = self.serializer(self.child_comment2).data
        self.assertEqual(serialized_comment.get('parent_comment'), expected_data)
    
    def test_expected_data_with_parent_comment_deleted(self):
        self.child_comment.delete()
        comment = Comment.objects.get(text="this is the text")
        serialized_comment = self.serializer(comment).data
        expected_data = {
            'owner' : '[deleted]',
            'date' : '[deleted]',
            'text' : '[deleted]',
            'uuid': '[deleted]'
        }
        self.assertEqual(serialized_comment.get('parent_comment'), expected_data)
    
    def test_is_valid_and_create_without_parent(self):
        data = {
            'text': 'this is a new comment',
            'user_id': self.sub.user.id,
            'commentfeed_uuid': str(self.commentfeed.uuid)
        }
        
        serializer = self.serializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        if serializer.is_valid():
            serializer.save()
        
        self.assertEqual(Comment.objects.count(), 5)
        
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
            'user_id': self.sub.user.id,
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
            'text': 'this is the new text',
            'user_id': self.sub.user.id
        }
        
        bad_data = {
            'text': 'this is not supposed to work',
            'user_id': 100
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