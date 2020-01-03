#serializer for Comment model
from django.contrib.auth.models import User

from rest_framework import serializers

from posts_app.models import Post, CommentFeed, Comment

from users_app.models import Sub

base_fields = ['uuid',  'liked', 'reported', 'user_id', 'has_parent',
        'is_original', 'parent_comment', 'text', 'likes', 'reports',
        'date', 'owner', 'id']

base_extra_kwargs = {
    'has_parent': {'read_only': True},
    'is_original': {'read_only': True},
    'id': {'read_only': True},
}
        

class BaseCommentSerializer(serializers.ModelSerializer):
    '''the base model for all comment serializers'''
    
    #read only fields
    uuid = serializers.CharField(source="get_uuid_as_string", read_only=True)
    liked = serializers.SerializerMethodField()
    reported = serializers.SerializerMethodField()
    date = serializers.CharField(source="get_date_posted", read_only=True)
    parent_comment = serializers.DictField(source="get_parent_comment", read_only=True)
    owner = serializers.DictField(source="get_owner_info", read_only=True)
    
    #write only fields
    user_id = serializers.IntegerField(write_only=True)
    
    def get_liked(self, obj):
        
        if self.context:
            session_sub = self.context['session_sub']
            if str(obj.uuid) in session_sub.liked_comments_as_list:
                return True
            else:
                return False
        else:
            return None
    
    def get_reported(self, obj):
        
        if self.context:
            session_sub = self.context['session_sub']
            
            if str(obj.uuid) in session_sub.reported_comments_as_list:
                return True
            else:
                return False
        else:
            return None


class OriginalCommentSerializer(BaseCommentSerializer):
    '''serializer for every comment that is supposed to be original'''
    
    #write only fields
    post_uuid = serializers.CharField(write_only=True, allow_null=True, default=None)
    
    class Meta:
        model = Comment
        fields = base_fields.copy()
        fields.append('post_uuid')
        extra_kargs = base_extra_kwargs
    
    def create(self, validated_data):
        puuid = validated_data.pop('post_uuid')
        usr_id = validated_data.pop('user_id')
        
        try:
            user = User.objects.get(id=usr_id)
            sub = Sub.objects.get(user=user)
            post = Post.objects.get(uuid=puuid)
        except User.DoesNotExist as e:
            raise Exception(e)
        except Sub.DoesNotExist as e:
            raise Exception(e)
        except Post.DoesNotExist as e:
            raise Exception(e)
        else:
            commentfeed = CommentFeed.objects.create(post=post)
            
            validated_data['commentfeed'] = commentfeed
            validated_data['owner'] = sub
            validated_data['is_original'] = True
            
            return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        #permissions should handle who can make updates
        usr_id = validated_data.pop('user_id')
        puuid = validated_data.pop('post_uuid')
        
        if usr_id != instance.owner.user.id or puuid != None:
            raise Exception("user_id cannot change and post_uuid must be None")
        else:
            new_text = validated_data.get('text')
            new_likes = validated_data.get('likes')
            new_reports = validated_data.get('reports')
            
            if new_text != instance.text:
                instance.text = new_text
            
            if new_likes != instance.likes and new_likes != None:
                instance.likes = new_likes
            
            if new_reports != instance.reports and new_reports != None:
                instance.reports = new_reports
            
            instance.save()
            return instance


class ChildCommentSerializer(BaseCommentSerializer):
    '''serializer for all children comments'''
    
    #write only fields
    commentfeed_uuid = serializers.CharField(
        write_only=True,
        allow_null=True,
        default=None
    )
    parent_uuid = serializers.CharField(write_only=True, allow_null=True, default=None)
    
    class Meta:
        model = Comment
        fields = base_fields.copy()
        fields.append('commentfeed_uuid')
        fields.append('parent_uuid')
        extra_kargs = base_extra_kwargs
    
    def create(self, validated_data):
        usr_id = validated_data.pop('user_id')
        cfuuid = validated_data.pop('commentfeed_uuid')
        pauuid = validated_data.pop('parent_uuid')
        
        try:
            user = User.objects.get(id=usr_id)
            sub = Sub.objects.get(user=user)
            commentfeed = CommentFeed.objects.get(uuid=cfuuid)
            
            if pauuid != None:
                parent_comment = Comment.objects.get(uuid=pauuid)
        
        except Sub.DoesNotExist as e:
            raise Exception(e)
        except User.DoesNotExist as e:
            raise Exception(e)
        except Comment.DoesNotExist as e:
            raise Exception(e)
        except CommentFeed.DoesNotExist as e:
            raise Exception(e)
        else:
            
            validated_data['owner'] = sub
            validated_data['commentfeed'] = commentfeed
            validated_data['is_original'] = False
            
            if pauuid != None:
                validated_data['parent_comment'] = parent_comment
                validated_data['has_parent'] = True
            else:
                validated_data['parent_comment'] = None
                validated_data['has_parent'] = False
            
            return Comment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        user_id = validated_data.pop('user_id')
        cfuuid = validated_data.pop('commentfeed_uuid')
        pauuid = validated_data.pop('parent_uuid')
        
        if user_id != instance.owner.user.id or cfuuid != None or pauuid != None:
            m = "user_id cannot change, commentfeed_uuid and parent_uuid must be None"
            raise Exception(m)
        else:
            new_text = validated_data.get('text')
            new_likes = validated_data.get('likes')
            new_reports = validated_data.get('reports')
            
            if new_text != instance.text:
                instance.text = new_text
            
            if new_likes != instance.likes and new_likes != None:
                instance.likes = new_likes
            
            if new_reports != instance.reports and new_reports != None:
                instance.reports = new_reports
            
            instance.save()
            return instance