'''posts_app.models'''
import uuid

from django.db import models
from django.utils.dateformat import DateFormat
from django.db.models.query import QuerySet

from users_app.models import Sub

from taggit.managers import TaggableManager


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
        '''return a list containing the slug of every community in communities'''
        return [com.slug for com in self.communities.all()]

    @property
    def get_owner_info(self):
        '''return a dict containing owner info
            (foreign key owner has property to do this)'''
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
    def get_date_posted(self) -> str:
        '''return a formatted string representing date'''
        return DateFormat(self.date_posted).format("M d, Y")
    
    @property
    def get_uuid_as_string(self) -> str:
        '''return uuid as string'''
        return str(self.uuid)
    
    @property
    def get_commentfeeds(self) -> "QuerySet['CommentFeed']":
        '''return a queryset of all CommentFeed objects related
            related to post instance'''
        return CommentFeed.objects.filter(post=self).order_by('-id')
    
    def __str__(self):
        return self.title[0:50]


class CommentFeed(models.Model):
    '''CommentFeed model'''

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    @property
    def get_post_uuid(self):
        '''return the post uuid as string
            (post foreign key has property to do this)'''
        return self.post.get_uuid_as_string
    
    @property
    def get_uuid_as_string(self):
        '''return uuid as string'''
        return str(self.uuid)
    
    @property
    def get_original_comment(self):
        '''return a queryset containing the only
            Comment object to have is_original as True'''
        #return the original comment, there should only be on per CommentFeed
        return Comment.objects.get(commentfeed=self, is_original=True)

    @property
    def get_children_comments(self):
        '''return all comments that have is_original is False'''
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
        '''get commentfeed foreign key uuid as string'''
        return self.commentfeed.get_uuid_as_string
    
    @property
    def get_owner_info(self):
        '''get dict containing owner info'''
        if self.owner:
            return {
                'username': self.owner.user.username,
                'uuid': self.owner.get_uuid_as_string
            }

        return {
            'username': "[deleted]",
            'uuid': None
        }
    
    @property
    def get_pic(self):
        '''return pic url'''
        if self.owner:
            return self.owner.get_profile_pic_url
        return None
    
    @property
    def get_parent_comment(self):
        '''return dict containing info about parent_comment'''
        if self.has_parent:
            if self.parent_comment:
                return {
                    'text': self.parent_comment.text,
                    'owner': self.parent_comment.get_owner_info,
                    'date': self.parent_comment.get_date_posted,
                    'uuid': self.parent_comment.get_uuid_as_string
                }
            
            else:
                return {
                    'text' : '[deleted]',
                    'owner' : '[deleted]',
                    'date' : '[deleted]',
                    'uuid' : '[deleted]'
                }
        return None
    
    @property
    def get_uuid_as_string(self):
        '''return uuid as string'''
        return str(self.uuid)
    
    @property
    def get_date_posted(self):
        '''return date as formatted string'''
        return DateFormat(self.date_posted).format("M d, Y")

    def __str__(self):
        return self.text[0:50]