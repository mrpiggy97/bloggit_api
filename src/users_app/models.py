#users_app models

from django.db import models
from django.contrib.auth.models import User
from django.utils.dateformat import DateFormat

from posts_app.models import Post, Comment

from taggit.managers import TaggableManager

import json
import uuid

class Sub(models.Model):
    '''sub model'''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="media/pics", null=True, default=None)
    liked_posts = models.TextField(default="[]")
    liked_comments = models.TextField(default="[]")
    reported_posts = models.TextField(default="[]")
    reported_comments = models.TextField(default="[]")
    communities = TaggableManager(blank=True)
    cake_day = models.DateTimeField(auto_now_add=True)
    reports = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    @property
    def get_username(self):
        return self.user.username
    
    @property
    def get_profile_pic(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return None
    
    @property
    def get_cake_day(self):
        return DateFormat(self.cake_day).format("M d, Y")
    
    @property
    def get_communities_as_list(self):
        return [com.slug for com in self.communities.all()]
    
    @property
    def get_uuid_as_string(self):
        return str(self.uuid)
    
    @property
    def get_posts(self):
        return Post.objects.filter(owner=self).order_by('-id')[0:250]
    
    @property
    def get_comments(self):
        return Comment.objects.filter(owner=self).order_by('-id')[0:250]
    
    @property
    def liked_posts_as_list(self):
        return json.loads(self.liked_posts)
    
    @liked_posts_as_list.setter
    def liked_posts_as_json(self, uuid_list):
        self.liked_posts = json.dumps(uuid_list)
        self.save()
    
    @property
    def liked_comments_as_list(self):
        return json.loads(self.liked_comments)
    
    @liked_comments_as_list.setter
    def liked_comments_as_json(self, uuid_list):
        self.liked_comments_as_json = json.dumps(uuid_list)
        self.save()
    
    @property
    def reported_posts_as_list(self):
        return json.loads(self.reported_posts)
    
    @reported_posts_as_list.setter
    def reported_posts_as_json(self, uuid_list):
        self.reported_posts = json.dumps(uuid_list)
        self.save()
    
    @property
    def reported_comments_as_list(self):
        return json.loads(self.reported_comments)
    
    @reported_comments_as_list.setter
    def reported_comments_as_json(self, uuid_list):
        self.reported_comments = json.dumps(uuid_list)
        self.save()
    

    def __str__(self):
        return self.user.username
    
