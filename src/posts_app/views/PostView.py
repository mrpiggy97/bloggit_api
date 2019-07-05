from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from posts_app.models import Post
from posts_app.serializers import PostSerializer

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication
from bloggit_project.utils.permissions import ReadOrOwnerOnly

import json



class PostView(APIView):
    '''generic class'''

    permission_classes = (ReadOrOwnerOnly,)
    authentication_classes = (CustomJSONWebTokenAuthentication,)
    serializer = PostSerializer

    def get_object(self):
        '''get post object'''

        try:
            uuid = self.kwargs['post_uuid']
            post = Post.objects.get(uuid=uuid)
        
        except Post.DoesNotExist:
            print("guck")
            return Response(data="shit", status=status.HTTP_404_NOT_FOUND)
        
        else:
            print(post.owner.user.username, self.request.user.username)
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

        post = self.get_object()
        context = self.get_serializer_context()
        data = self.serializer(post, context=context).data

        return Response(data=json.dumps(data), status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):

        post = self.get_object()
        data = json.loads(request.data)
        context = self.get_serializer_context()
        serializer = self.serializer(post, data=data, context=context)

        if serializer.is_valid():
            serializer.save()
            json_data = json.dumps(serializer.data)
            return Response(data=json_data, status=status.HTTP_200_OK)
        else:
            return Response(data=None, status=status.HTTP_501_NOT_IMPLEMENTED)