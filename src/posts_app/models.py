#posts_app.models

from django.db import models
from django.utils.dateformat import DateFormat

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
    def get_communities_as_list(self):
        return [com.slug for com in self.communities.all()]

    @property
    def get_owner_info(self):
        if self.owner:
            return {
                'username': self.owner.user.username,
                'profile_pic': self.owner.get_profile_pic_url,
                'uuid': self.owner.get_uuid_as_string
            }
        else:
            return {
                'username': "[deleted]",
                'profile_pic': None,
                'uuid': None
            }
    
    @property
    def get_date_posted(self):
        return DateFormat(self.date_posted).format("M d, Y")
    
    @property
    def get_uuid_as_string(self):
        return str(self.uuid)
    
    @property
    def get_commentfeeds(self):
        return CommentFeed.objects.filter(post=self).order_by('-id')
    
    def __str__(self):
        return self.title[0:50]


class CommentFeed(models.Model):
    '''CommentFeed model'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    @property
    def get_post_uuid(self):
        return self.post.get_uuid_as_string
    
    @property
    def get_uuid_as_string(self):
        return str(self.uuid)
    
    @property
    def get_original_comment(self):
        #return the original comment, there should only be on per CommentFeed
        return Comment.objects.get(commentfeed=self, is_original=True)

    @property
    def get_children_comments(self):
        #return all comments that have is_original is False
        return Comment.objects.filter(commentfeed=self, is_original=False).order_by('-id')


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
    def get_commentfeed_uuid(self):
        return self.commentfeed.get_uuid_as_string
    
    @property
    def get_owner_info(self):
        if self.owner:
            return {
                'username': self.owner.user.username,
                'uuid': self.owner.get_uuid_as_string
            }
        else:
            return {
                'username': "[deleted]",
                'uuid': None
            }
    
    @property
    def get_pic(self):
        if self.owner:
            return self.owner.get_profile_pic_url
        else:
            return None
    
    @property
    def get_parent_comment(self):
        
        if self.has_parent == True:
            if self.parent_comment:
                return {
                    'title': self.parent_comment.title,
                    'text': self.parent_comment.text,
                    'username': self.parent_comment.get_username,
                    'date': self.parent_comment.get_date_posted,
                    'uuid': self.parent_comment.get_uuid_as_string
                }
            
            else:
                return None
        else:
            return None
    
    @property
    def get_uuid_as_string(self):
        return str(self.uuid)
    
    @property
    def get_date_posted(self):
        return DateFormat(self.date_posted).format("M d, Y")

    def __str__(self):
        return self.text[0:50]