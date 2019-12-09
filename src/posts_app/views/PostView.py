from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from posts_app.models import Post, CommentFeed
from posts_app.serializers.PostSerializer import PostSerializer
from posts_app.serializers.CommentFeedSerializer import CommentFeedSerializer

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication
from bloggit_project.utils.permissions import AuthenticatedReadAndOwnerOnly
import json


class PostView(APIView):
    '''generic class'''

    permission_classes = (AuthenticatedReadAndOwnerOnly,)
    authentication_classes = (CustomJSONWebTokenAuthentication,)
    post_serializer = PostSerializer
    commentfeed_serializer = CommentFeedSerializer

    def get_object(self):
        '''get post object'''

        try:
            uuid = self.kwargs['post_uuid']
            post = Post.objects.get(uuid=uuid)
        
        except Post.DoesNotExist:
            return Response(data="shit", status=status.HTTP_404_NOT_FOUND)
        
        else:
            self.check_object_permissions(self.request, post)
            return post
    

    def get_serializer_context(self):
        '''return a context for the serializer'''

        if self.request.user.is_authenticated:
            session_sub = Sub.objects.get(user=self.request.user)
            return {'session_sub': session_sub}
        else:
            return None
    
    def get_invalid_message(self):
        return "sorry there was an error with the data provided"
    

    def get(self, request, *args, **kwargs):
        '''return post object along with all commentfeeds related to it'''

        post = self.get_object()
        commentfeeds = post.get_commentfeeds
        context = self.get_serializer_context()
        post_data = self.post_serializer(post, context=context).data
        commentfeed_data = self.commentfeed_serializer(commentfeeds,
                                                        context=context,
                                                        many=True).data
        data = {
            'posts': post_data,
            'commentfeeds': commentfeed_data,
            'authenticated': request.user.is_authenticated
        }
        
        status_code = status.HTTP_200_OK

        return Response(data=data, status=status_code)
    
    def put(self, request, *args, **kwargs):
        post = self.get_object()
        data = request.data
        data['user_id'] = request.user.id
        context = self.get_serializer_context()
        serializer = self.post_serializer(post, data=data, context=context)

        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_200_OK
            return Response(data=None, status=status_code)
        else:
            d = {
                'message': self.get_invalid_message()
            }
            return Response(data=d, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        data = request.data
        data['user_id'] = request.user.id
        context = self.get_serializer_context()
        serializer = self.post_serializer(data=data, context=context)
        
        if serializer.is_valid():
            serializer.save()
            status_code = status.HTTP_201_CREATED
            return Response(data=serializer.data, status=status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            d = {
                'message': self.get_invalid_message()
            }
            return Response(data=d, status=status_code)
    
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(data=None, status=status.HTTP_200_OK)