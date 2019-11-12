#this will test the original comment serializer

from rest_framework.test import APITestCase

from posts_app.models import Post, CommentFeed, Comment
from posts_app.serializers.CommentSerializer import OriginalCommentSerializer
from posts_app.tests.utils import (create_post, create_sub, create_user,
                                   create_original_comment)

class TestOriginalCommentSerializer(APITestCase):
    '''test how the data looks, the creation and updating'''
    '''of an original comment through OriginalCommentSerializer'''
    
    def setUp(self):
        
        self.user = create_user()
        self.sub = create_sub(self.user)
        self.post = create_post(self.sub)
        self.commentfeed = CommentFeed.objects.create(post=self.post)
        self.first_comment = create_original_comment(self.post, self.sub)
        
        self.expected_data1 = {
            'uuid': self.first_comment.get_uuid_as_string,
            'liked': None,
            'reported': None,
            'date': self.first_comment.get_date_posted,
            'parent_comment': self.first_comment.get_parent_comment,
            'pic': self.first_comment.get_pic,
            'owner': self.first_comment.get_owner_info,
            'has_parent': False,
            'is_original': True,
            'text': self.first_comment.text,
            'likes': self.first_comment.likes,
            'reports': self.first_comment.reports
        }
        
        self.expected_data2 = self.expected_data1.copy()
        self.expected_data2['liked'] = False
        self.expected_data2['reported'] = False
        
        self.serializer = OriginalCommentSerializer
    
    def test_expected_data(self):
        
        data1 = self.serializer(self.first_comment, context=None).data
        
        context = {'session_sub': self.sub}
        data2 = self.serializer(self.first_comment, context=context).data
        
        self.assertIsNotNone(data1)
        self.assertEqual(data1, self.expected_data1)
        self.assertEqual(data2, self.expected_data2)
    
    def test_is_valid_and_create(self):
        '''test is_valid and create methods from serializer'''
        
        #this data should be valid
        data = {
            'owner_uuid': str(self.sub.uuid),
            'post_uuid': str(self.post.uuid),
            'text': 'this is the second comment',
        }
        
        #while this data might be valid its supposed to throw an error
        bad_data = {
            'owner_uuid': None,
            'post_uuid': str(self.sub.uuid),
            'text': 'this is not supposed to work'
        }
        
        context = {'session_sub': self.sub}
        
        serializer = self.serializer(data=data, context=context)
        self.assertTrue(serializer.is_valid())
        
        if serializer.is_valid():
            serializer.save()
        
        self.assertTrue(Comment.objects.count(), 2)
        
        serializer2 = self.serializer(data=bad_data, context=context)
        self.assertTrue(serializer2.is_valid())
        
        self.assertRaises(Exception, serializer2.create, bad_data)
    
    def test_udpate(self):
        '''test update method from serializer'''
        
        data = {
            'text': 'this is the edited text'
        }
        
        bad_data = {
            'owner_uuid': str(self.sub.uuid),
            'text': 'this is not supposed to work'
        }
        
        serializer = self.serializer(self.first_comment, data=data, context=None)
        self.assertTrue(serializer.is_valid())
        
        if serializer.is_valid():
            serializer.save()
        
        comment = Comment.objects.first()
        self.assertEqual(comment.text, data['text'])
        
        serializer2 = self.serializer()
        
        self.assertRaises(Exception, serializer2.update, bad_data)