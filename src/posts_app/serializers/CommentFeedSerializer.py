#serializer for CommentFeed model

from rest_framework import serializers

from posts_app.models import Post, CommentFeed
from posts_app.serializers.CommentSerializer import (OriginalCommentSerializer,
                                                     ChildCommentSerializer)

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
            return OriginalCommentSerializer(comment, context=context).data
        
        else:
            return OriginalCommentSerializer(comment, context=None).data
    
    def get_children_comments(self, obj):
        #get all comments that have is_original is False

        comments = obj.get_children_comments

        if self.context:
            session_sub = self.context['session_sub']
            context = {'session_sub': session_sub}
            return ChildCommentSerializer(comments, context=context, many=True).data
        
        else:
            return ChildCommentSerializer(comments, context=None, many=True).data
    
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