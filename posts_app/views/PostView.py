from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from posts_app.models import Post, CommentFeed
from posts_app.serializers.PostSerializer import PostSerializer
from posts_app.serializers.CommentFeedSerializer import CommentFeedSerializer

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication
from bloggit_project.utils.permissions import ReadOrOwnerOnly

import json



class PostView(APIView):
    '''generic class'''

    permission_classes = (ReadOrOwnerOnly,)
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
    

    def get(self, request, *args, **kwargs):
        '''return post object along with all commentfeeds related to it'''

        post = self.get_object()
        commentfeeds = post.get_commentfeeds
        context = self.get_serializer_context()
        post_data = self.post_serializer(post, context=context).data
        commentfeed_data = self.commentfeed_serializer(commentfeeds,
                                                        context=context,
                                                        many=True).data
        json_data = json.dumps({
            'posts': post_data,
            'commentfeeds': commentfeed_data
        })

        return Response(
            data=json_data,
            status=status.HTTP_200_OK,
            content_type='json'
            )
    
    def put(self, request, *args, **kwargs):

        post = self.get_object()
        data = json.loads(request.data)
        context = self.get_serializer_context()
        serializer = self.post_serializer(post, data=data, context=context)

        if serializer.is_valid():
            serializer.save()
            json_data = json.dumps(serializer.data)
            return Response(data=json_data,
                            status=status.HTTP_200_OK,
                            content_type='json')
        else:
            return Response(data=None, status=status.HTTP_304_NOT_MODIFIED)
    
    def post(self, request, *args, **kwargs):

        data = json.loads(request.data)
        context = self.get_serializer_context()
        serializer = self.post_serializer(data=data, context=context)
        
        if serializer.is_valid():
            serializer.save()
            response_data = json.dumps(serializer.data)
            return Response(data=response_data,
                            status=status.HTTP_201_CREATED,
                            content_type='json')
        else:
            return Response(data=None,
                            status=status.HTTP_501_NOT_IMPLEMENTED,
                            content_type='json')
    
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(data=None, status=status.HTTP_200_OK)