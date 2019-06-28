#posts_app serializers

from rest_framework import serializers

from .models import Post, CommentFeed, Comment

from users_app.models import Sub

class PostSerializer(serializers.ModelSerializer):
    '''serializer for Post model'''

    #read only fields
    communities_list = serializers.ListField(source="get_communities_as_list",
                                                read_only=True)
    username = serializers.CharField(source="get_username", read_only=True)
    pic = serializers.CharField(source="get_pic", read_only=True)
    date = serializers.CharField(source="get_date_posted", read_only=True)
    uuid = serializers.CharField(source="get_uuid_as_string", read_only=True)
    liked = serializers.SerializerMethodField()
    reported = serializers.SerializerMethodField()

    #write only fields
    owner_uuid = serializers.CharField(write_only=True)
    add_communities = serializers.ListField(allow_null=True,
                                            default=None, write_only=True)

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
    

    class Meta:
        model = Post
        fields = ['communities_list', 'username', 'pic', 'date', 'uuid',
                    'liked', 'reported', 'owner_uuid', 'add_communities',
                    'title', 'text', 'text', 'likes', 'reports']
    

    def create(self, validated_data):
        #try to get Sub from uuid given in validate_data
        try:
            owner = Sub.objects.get(uuid=validated_data.pop('owner_uuid'))
            communities = validated_data.pop('add_communities')
        #if no sub has that uuid return None
        except Sub.DoesNotExist:
            print("sorry that user does not seem to exist")
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

        if uuid == str(instance.uuid):
            instance.title = validated_data['title']
            instance.text = validated_data['text']
            instance.save()
            return instance
        else:
            return None
