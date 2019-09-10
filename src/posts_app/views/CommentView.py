#retrieve update, create and update a comment object

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from posts_app.models import Comment, CommentFeed
from posts_app.serializers.CommentSerializer import CommentSerializer

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication
from bloggit_project.utils.permissions import ReadOrOwnerOnly
import json

class CommentView(APIView):
    '''retrieve update create and delete comment'''

    serializer = CommentSerializer
    permission_classes = (ReadOrOwnerOnly,)
    authentication_classes = (CustomJSONWebTokenAuthentication,)

    def get_object(self):
        uuid = self.kwargs['comment_uuid']
        
        try:
            comment = Comment.objects.get(uuid=uuid)
        
        except Comment.DoesNotExist:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        
        else:
            self.check_object_permissions(self.request, comment)
            return comment
    
    def get_serializer_context(self):

        if self.request.user.is_authenticated:
            session_sub = Sub.objects.get(user=self.request.user)
            return {'session_sub': session_sub}
        
        elif self.request.user.is_anonymous:
            return None
    
    def get(self, request, *args, **kwargs):
        '''get comment'''

        comment = self.get_object()
        context = self.get_serializer_context()
        data = self.serializer(comment, context=context).data
        data['authenticated'] = request.user.is_authenticated
        status_code = status.HTTP_200_OK

        return Response(data=data, status=status_code)
    
    def post(self, request, *args, **kwargs):

        data = json.loads(request.POST['data'])
        context = self.get_serializer_context()
        serializer = self.serializer(data=data, context=context)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            status_code = status.HTTP_201_CREATED

            return Response(data=data, status=status_code)
        else:
            return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        '''update comment instance'''

        comment = self.get_object()
        context = self.get_serializer_context()
        data = json.loads(request.data)
        serializer = self.serializer(comment, data=data, context=context)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            status_code = status.HTTP_200_OK

            return Response(data=data, status=status_code)
        else:
            return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        '''delete comment'''

        comment = self.get_object()
        comment.delete()
        return Response(data=None, status=status.HTTP_200_OK)
            