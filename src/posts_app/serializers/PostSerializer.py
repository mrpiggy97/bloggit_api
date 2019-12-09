#serializer for Post model
from django.contrib.auth.models import User

from rest_framework import serializers

from posts_app.models import Post

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
    user_id = serializers.IntegerField(write_only=True)
    add_communities = serializers.ListField(allow_null=True,
                                            default=None, write_only=True)
    
    remove_communities = serializers.ListField(write_only=True,
                                               allow_null=True,
                                               default=None)

    class Meta:
        model = Post
        fields = ['communities_list', 'owner', 'pic', 'date', 'uuid',
                    'liked', 'reported', 'user_id', 'add_communities',
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
        
        #try to get user from user_id to then get the corresponding
        #sub
        try:
            user = User.objects.get(id=validated_data.pop('user_id'))
            owner = Sub.objects.get(user=user)
        except User.DoesNotExist as e:
            raise Exception(e)
        except Sub.DoesNotExist as e:
            raise Exception(e)
        else:
            new_post = Post.objects.create(**validated_data, owner=owner)

            if communities:
                for com in communities:
                    new_post.communities.add(com)
            return new_post
    
    def update(self, instance, validated_data):

        usr_id = validated_data.pop('user_id')

        if usr_id == instance.owner.user.id:
            instance.title = validated_data['title']
            instance.text = validated_data['text']

            if validated_data['remove_communities']:
                for com in validated_data['remove_communities']:
                    instance.communities.remove(com)
            instance.save()
            return instance
        else:
            message = "user_id has to be the same as owner's user id"
            raise Exception(message)