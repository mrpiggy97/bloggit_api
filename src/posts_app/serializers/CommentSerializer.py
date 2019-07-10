#serializer for Comment model

from rest_framework import serializers

from posts_app.models import CommentFeed, Comment

from users_app.models import Sub


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