#serializer for Comment model

from rest_framework import serializers

from posts_app.models import Post, CommentFeed, Comment

from users_app.models import Sub

base_fields = ['uuid',  'liked', 'reported', 'owner_uuid', 'has_parent',
        'is_original', 'parent_comment', 'text', 'likes', 'reports',
        'date', 'pic', 'owner', 'id']

base_extra_kwargs = {
    'has_parent': {'read_only': True},
    'is_original': {'read_only': True},
    'id': {'read_only': True}
}
        

class BaseCommentSerializer(serializers.ModelSerializer):
    '''the base model for all comment serializers'''
    
    #read only fields
    uuid = serializers.CharField(source="get_uuid_as_string", read_only=True)
    liked = serializers.SerializerMethodField()
    reported = serializers.SerializerMethodField()
    date = serializers.CharField(source="get_date_posted", read_only=True)
    parent_comment = serializers.DictField(source="get_parent_comment", read_only=True)
    pic = serializers.CharField(source="get_pic", read_only=True)
    owner = serializers.DictField(source="get_owner_info", read_only=True)
    
    #write only fields
    owner_uuid = serializers.CharField(write_only=True, allow_null=True, default=None)
    
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
        owuuid = validated_data.pop('owner_uuid')
        
        if puuid == None or owuuid == None:
            raise Exception("please provide both uuid's for owner and post")
        else:
        
            post = Post.objects.get(uuid=puuid)
            commentfeed = CommentFeed.objects.create(post=post)
            
            session_sub = Sub.objects.get(uuid=owuuid)
            
            validated_data['commentfeed'] = commentfeed
            validated_data['owner'] = session_sub
            validated_data['is_original'] = True
            
            return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        #permissions should handle who can make updates
        
        puuid = validated_data.pop('post_uuid')
        owuuid = validated_data.pop('owner_uuid')
        
        if puuid != None or owuuid != None:
            raise Exception("owner_uuid and post_uuid must be None when updating")
        else:
            if instance.text != validated_data['text']:
                instance.text = validated_data['text']
            
            try:
                new_likes = validated_data['likes']
            except KeyError:
                pass
            else:
                instance.likes = new_likes
            
            try:
                new_reports = validated_data['reports']
            except KeyError:
                pass
            else:
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
        owuuid = validated_data.pop('owner_uuid')
        cfuuid = validated_data.pop('commentfeed_uuid')
        pauuid = validated_data.pop('parent_uuid')
        
        if owuuid == None or cfuuid == None:
            raise Exception("uuid for owner and commentfeed have to be provided")
        else:
        
            session_sub = Sub.objects.get(uuid=owuuid)
            commentfeed = CommentFeed.objects.get(uuid=cfuuid)
            
            if pauuid != None:
                parent_comment = Comment.objects.get(uuid=pauuid)
                validated_data['parent_comment'] = parent_comment
                validated_data['has_parent'] = True
            else:
                validated_data['has_parent'] = False
                validated_data['parent_comment'] = None
            
            validated_data['owner'] = session_sub
            validated_data['commentfeed'] = commentfeed
            validated_data['is_original'] = False
            
            return Comment.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        owuuid = validated_data.pop('owner_uuid')
        cfuuid = validated_data.pop('commentfeed_uuid')
        pauuid = validated_data.pop('parent_uuid')
        
        if owuuid != None or cfuuid != None or pauuid != None:
            print("when updating all owner uuid commentfeed uuid and/n")
            print("parent uuid fields must be None")
            raise ValueError
        else:
            if instance.text != validated_data['text']:
                instance.text = validated_data['text']
            
            try:
                new_likes = validated_data['likes']
            except KeyError:
                pass
            else:
                instance.likes = new_likes
            
            try:
                new_reports = validated_data['reports']
            except KeyError:
                pass
            else:
                instance.reports = new_reports
            
            instance.save()
            return instance