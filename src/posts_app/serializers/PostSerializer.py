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
        #remove_communities, add_communities and user_id are fields
        #that are not in Post model itself therefore they can't go into
        #Post.objects.create() method so we will take them away from
        #validated_data
        
        del validated_data['remove_communities']
        #communities are added to the model through the taggit api at the end
        communities = validated_data.pop('add_communities')
        
        #try to get user from user_id to then get the corresponding
        #Sub model that will be the post owner
        try:
            #user_id cannot be supplied by the front end, it should always
            #be provided by the corresponding views that serves to create and
            #update posts
            usr_id = validated_data.pop('user_id')
            user = User.objects.get(id=usr_id)
            sub = Sub.objects.get(user=user)
        except User.DoesNotExist as e:
            raise Exception(e)
        except Sub.DoesNotExist as e:
            raise Exception(e)
        else:
            validated_data['owner'] = sub
            new_post = Post.objects.create(**validated_data)
            if communities:
                for com in communities:
                    new_post.communities.add(com)
            return new_post
    
    def update(self, instance, validated_data):
        #user_id cannot be supplied by the front end, it shouold always be
        #provided by the corresponding views that serves to
        #update and create a post
        usr_id = validated_data.pop('user_id')

        if usr_id == instance.owner.user.id:
            new_title = validated_data.get('title')
            new_text = validated_data.get('text')
            new_likes = validated_data.get('likes')
            new_reports = validated_data.get('reports')
            
            if new_title != instance.title:
                instance.title = new_title
            
            if new_text != instance.text:
                instance.text = new_text
            
            if new_likes != instance.likes and new_likes != None:
                instance.likes = new_likes
            
            if new_reports != instance.reports and new_reports != None:
                instance.reports = new_reports

            if validated_data.get('remove_communities'):
                for com in validated_data.get('remove_communities'):
                    instance.communities.remove(com)
            instance.save()
            return instance
        else:
            message = "user_id cannot change"
            raise Exception(message)