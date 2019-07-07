#posts_app serializers

from rest_framework import serializers

from .models import Post, CommentFeed, Comment

from users_app.models import Sub

class PostSerializer(serializers.ModelSerializer):
    '''serializer for Post model'''

    #read only fields
    communities_list = serializers.ListField(source="get_communities_as_list",
                                                read_only=True)
    owner = serializers.DictField(source="get_owner_info", read_only=True)
    pic = serializers.CharField(source="get_pic", read_only=True)
    date = serializers.CharField(source="get_date_posted", read_only=True)
    uuid = serializers.CharField(source="get_uuid_as_string", read_only=True)
    liked = serializers.SerializerMethodField()
    reported = serializers.SerializerMethodField()

    #write only fields
    owner_uuid = serializers.CharField(write_only=True)
    add_communities = serializers.ListField(allow_null=True,
                                            default=None, write_only=True)
    
    remove_communities = serializers.ListField(write_only=True,
                                               allow_null=True,
                                               default=None)

    class Meta:
        model = Post
        fields = ['communities_list', 'owner', 'pic', 'date', 'uuid',
                    'liked', 'reported', 'owner_uuid', 'add_communities',
                    'remove_communities', 'title', 'text', 'likes', 'reports']

    def get_liked(self, obj):
        if self.context:
            session_sub = self.context['session_sub']

            if str(obj.uuid) in session_sub.liked_posts_as_list:
                return True
            else:
                return False
        else:
            return None
    
    def get_reported(self, obj):
        if self.context:
            session_sub = self.context['session_sub']
            
            if str(obj.uuid) in session_sub.reported_posts_as_list:
                return True
            else:
                return False
        else:
            return None
    

    def create(self, validated_data):

        del validated_data['remove_communities']
        communities = validated_data.pop('add_communities')
        
        #try to get sub from uuid goven in validated_data
        try:
            owner = Sub.objects.get(uuid=validated_data.pop('owner_uuid'))
        #if no sub has that uuid return None
        except Sub.DoesNotExist:
            return None
        #else create a new post
        else:
            new_post = Post.objects.create(**validated_data, owner=owner)

            if communities:
                for com in communities:
                    new_post.communities.add(com)
            return new_post
    
    def update(self, instance, validated_data):

        uuid = validated_data.pop('owner_uuid')

        if uuid == str(instance.owner.uuid):
            instance.title = validated_data['title']
            instance.text = validated_data['text']

            if validated_data['remove_communities']:
                for com in validated_data['remove_communities']:
                    instance.communities.remove(com)
            instance.save()
            return instance
        else:
            return None


class CommentFeedSerializer(serializers.ModelSerializer):
    '''serializer for CommentFeed model'''

    uuid = serializers.CharField(source="get_uuid_as_string", read_only=True)
    original_comment = serializers.SerializerMethodField()
    children_comments = serializers.SerializerMethodField()

    post_uuid = serializers.CharField(write_only=True)


    class Meta:
        model = CommentFeed
        fields = ['uuid', 'post_uuid', 'original_comment', 'children_comments']

    def get_original_comment(self, obj):
        #there should only be one original_comment per CommentFeed

        comment = obj.get_original_comment

        if self.context:
            session_sub = self.context['session_sub']
            context = {'session_sub': session_sub}
            return CommentSerializer(comment, context=context).data
        
        else:
            return CommentSerializer(comment).data
    
    def get_children_comments(self, obj):
        #get all comments that have is_original is False

        comments = obj.get_children_comments

        if self.context:
            session_sub = self.context['session_sub']
            context = {'session_sub': session_sub}
            return CommentSerializer(comments, context=context, many=True).data
        
        else:
            return CommentSerializer(comments, many=True).data
    
    def create(self, validate_data):
        try:
            post = Post.objects.get(uuid=validate_data['post_uuid'])
        
        except Post.DoesNotExist:
            return None
        
        else:
            return CommentFeed.objects.create(post=post)
    
    def update(self, instance, validate_data):
        #this serializer does not update data because
        #updating a CommentFeed object seems useless

        return None



class CommentSerializer(serializers.ModelSerializer):
    '''serializer for Comment model'''

    #read only fields
    uuid = serializers.CharField(source="get_uuid_as_string", read_only=True)
    owner = serializers.DictField(source="get_owner_info", read_only=True)
    pic = serializers.CharField(source="get_pic", read_only=True)
    parent_comment = serializers.DictField(source="get_parent_comment",
                                                allow_null=True, read_only=True)
    date = serializers.CharField(source="get_date_posted", read_only=True)
    liked = serializers.SerializerMethodField()
    reported = serializers.SerializerMethodField()

    #write only fields
    owner_uuid = serializers.CharField(write_only=True)
    commentfeed_uuid = serializers.CharField(write_only=True)

    class Meta:
        model = Comment
        fields = ['uuid', 'owner', 'pic', 'parent_comment', 'date', 'liked',
                    'reported', 'owner_uuid', 'commentfeed_uuid', 'text',
                    'has_parent', 'is_original', 'likes', 'reports']

    def get_liked(self, obj):
        '''check if obj uuid is in any Sub model liked_posts'''

        if self.context:
            session_sub = self.context['session_sub']
            
            if obj.get_uuid_as_string in session_sub.liked_comments_as_list:
                return True
            else:
                return False
        else:
            return None
    
    def get_reported(self, obj):

        if self.context:
            session_sub = self.context['session_sub']

            if obj.get_uuid_as_string in session_sub.reported_comments_as_list:
                return True
            else:
                return False
        else:
            return None

    def create(self, validate_data):
        #owner and commentfeed are foreign key fields
        #get them with the uuid given as string in
        #owner_uuid and commentfeed_uuid
        owner_uuid = validate_data.pop('owner_uuid')
        commentfeed_uuid = validate_data.pop('commentfeed_uuid')

        try:
            owner = Sub.objects.get(uuid=owner_uuid)
            commentfeed = CommentFeed.objects.get(uuid=commentfeed_uuid)

            fk_fields = {
                'owner': owner,
                'commentfeed': commentfeed
            }

        except (Sub.DoesNotExist, CommentFeed.DoesNotExist):
            return None
        
        else:
            comment =  Comment.objects.create(**validate_data, **fk_fields)
            return comment
    
    def update(self, instance, validate_data):
        #likes and reports dont't need to be provided they are optional
        #all other write fields don't change the instance provided
        #to the serializer

        #first check that owner_uuid and commentfeed_uuid
        #are the same as instance.owner.uuid and instance.commentfeed.uuid

        owner_uuid = validate_data.pop('owner_uuid')
        commentfeed_uuid = validate_data.pop('commentfeed_uuid')

        valid_owner = owner_uuid == str(instance.owner.uuid)
        valid_commentfeed = commentfeed_uuid == str(instance.commentfeed.uuid)

        if valid_owner and valid_commentfeed:
            instance.text = validate_data['text']

            if validate_data['likes']:
                instance.likes = validate_data['likes']
            
            if validate_data['reports']:
                instance.reports = validate_data['reports']

            instance.save()

            return instance
        
        else:
            return None


