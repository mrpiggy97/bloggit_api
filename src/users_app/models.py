#users_app models

from django.db import models
from django.contrib.auth.models import User
from django.utils.dateformat import DateFormat

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
    def get_profile_pic_url(self):
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
    def liked_posts_as_list(self):
        return json.loads(self.liked_posts)
    
    @liked_posts_as_list.setter
    def liked_posts_as_list(self, like_list):
        self.liked_posts = json.dumps(like_list)
        self.save()
    
    @property
    def liked_comments_as_list(self):
        return json.loads(self.liked_comments)
    
    @liked_comments_as_list.setter
    def liked_comments_as_list(self, like_list):
        self.liked_comments = json.dumps(like_list)
        self.save()
    
    @property
    def reported_posts_as_list(self):
        return json.loads(self.reported_posts)
    
    @reported_posts_as_list.setter
    def reported_posts_as_list(self, report_list):
        self.reported_posts = json.dumps(report_list)
        self.save()
    
    @property
    def reported_comments_as_list(self):
        return json.loads(self.reported_comments)
    
    @reported_comments_as_list.setter
    def reported_comments_as_list(self, report_list):
        self.reported_comments = json.dumps(report_list)
        self.save()

    def __str__(self):
        return self.user.username
    
