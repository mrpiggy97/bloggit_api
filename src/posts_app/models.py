#posts_app.models

from django.db import models
from django.utils.dateformat import DateFormat

from .serializers import CommentSerializer

from users_app.models import Sub

from taggit.managers import TaggableManager

import uuid
import json


class Post(models.Model):
    '''post model'''

    title = models.TextField(max_length=200)
    text = models.TextField(max_length=700)
    communities = TaggableManager()
    owner = models.ForeignKey(Sub, null=True, on_delete=models.SET_NULL)
    date_posted = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    likes = models.IntegerField(default=1)
    reports = models.IntegerField(default=0)

    @property
    def get_username(self):
        if self.owner:
            return self.owner.user.username
        else:
            return "[deleted]"
    
    @property
    def get_pic(self):
        #get profile picture url from sub.profile_picture

        if self.owner:
            return self.owner.get_profile_pic
        else:
            return None
    
    @property
    def get_date_posted(self):
        return DateFormat(self.date_posted).format("M d, Y")
    
    @property
    def get_communities_as_list(self):
        return [com.slug for com in self.communities.slug]
    
    def __str__(self):
        return self.title[0:50]


class CommentFeed(models.Model):
    '''CommentFeed model'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    @property
    def get_post_uuid(self):
        return self.post.uuid
    
    def get_original_comment_serialized(self, session_sub):

        try:
            original_comment = Comment.objects.get(commentfeed=self, is_original=True)
        except Comment.DoesNotExist:
            original_comment = None
            return None
        else:
            context = {'session_sub': session_sub}
            serialized_comment = CommentSerializer(original_comment, context=context)
            return serialized_comment.data
    
    def get_children_comments_serialized(self, session_sub):

        comments = Comment.objects.filter(commentfeed=self, is_original=False)
        context = {'session_sub': session_sub}
        serialized_comments = CommentSerializer(comments, context=context, multiple=True)
        return serialized_comments.data

    def __str__(self):
        return "comment feed for %s" %(self.post.get_uuid_as_string)


class Comment(models.Model):
    '''comment model'''

    commentfeed = models.ForeignKey(CommentFeed, on_delete=models.CASCADE)
    owner = models.ForeignKey(Sub, null=True, on_delete=models.SET_NULL)
    parent_comment = models.ForeignKey('self', null=True, default=None,
                                            on_delete=models.SET_NULL)
    text = models.TextField(max_length=700)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_original = models.BooleanField(default=True)
    has_parent = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=1)
    reports = models.IntegerField(default=0)
    
    @property
    def get_username(self):
        if self.owner:
            return self.owner.user.username
        else:
            return "[deleted]"
    
    @property
    def get_pic(self):
        if self.owner:
            return self.owner.get_profile_pic
        else:
            return None
    
    @property
    def get_date_posted(self):
        return DateFormat(self.date_posted).format("M d, Y")
    
    @property
    def get_parent_comment(self):
        if self.has_parent:
            if self.parent_comment:
                return {
                    'username': self.parent_comment.get_username,
                    'date': self.parent_comment.get_date_posted,
                    'text': self.parent_comment.text
                }
            
            else:
                return "[deleted]"
        
        else:
            return None

    def __str__(self):
        return self.text[0:50]