from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from posts_app.models import Post, Comment
from posts_app.serializers.CommentSerializer import (OriginalCommentSerializer,
                                                     ChildCommentSerializer)

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication
from bloggit_project.utils.permissions import AuthenticatedReadAndOwnerOnly

class CommentView(APIView):
    
    original_serializer = OriginalCommentSerializer
    child_serializer = ChildCommentSerializer
    authentication_classes = (CustomJSONWebTokenAuthentication,)
    permission_classes = (AuthenticatedReadAndOwnerOnly,)
    
    def get_object(self):
        
        comment_uuid = self.kwargs['comment_uuid']
        
        try:
            comment = Comment.objects.get(uuid=comment_uuid)
        
        except Comment.DoesNotExist:
            status_code = status.HTTP_404_NOT_FOUND
            return Response(data=None, status=status_code)
        else:
            self.check_object_permissions(self.request, comment)
            return comment
    
    def get_serializer_context(self):
        
        if self.request.user.is_authenticated:
            session_sub = Sub.objects.get(user=self.request.user)
            return {'session_sub': session_sub}
        else:
            return None
    
    def get_invalid_message(self):
        return 'invalid data'
    
    def get(self, request, *args, **kwargs):
        
        comment = self.get_object()
        context = self.get_serializer_context()
        
        if comment.is_original:
            serializer = OriginalCommentSerializer(comment, context=context)
        else:
            serializer = ChildCommentSerializer(comment, context=context)
        
        status_code = status.HTTP_200_OK
        data = {
            'authenticated': request.user.is_authenticated,
            'comment': serializer.data
        }
        return Response(data=data, status=status_code)

    def post(self, request, *args, **kwargs):
        
        data = request.data
        context = self.get_serializer_context()
        
        if kwargs.get('is_original') == True:
            serializer = OriginalCommentSerializer(data=data, context=context)
        else:
            serializer = ChildCommentSerializer(data=data, context=context)
        
        if serializer.is_valid():
            
            if kwargs.get('is_original') == True:
                if data.get('post_uuid') == None or data.get('owner_uuid') == None:
                    status_code = status.HTTP_400_BAD_REQUEST
                    data = {
                        'message': 'you must provide post_uuid and owner_uuid'
                    }
                    return Response(data=data, status=status_code)
            elif kwargs.get('is_original') == False:
                if data.get('commentfeed_uuid') == None or data.get('owner_uuid') == None:
                    status_code = status.HTTP_400_BAD_REQUEST
                    data = {
                        'message': 'you must provide commentfeed_uuid and owner_uuid'
                    }
                    return Response(data=data, status=status_code)
                
            status_code = status.HTTP_201_CREATED
            serializer.save()
            return Response(data=serializer.data, status=status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            data = {
                'message': self.get_invalid_message()
            }
            return Response(data=data, status=status_code)
    
    def put(self, request, *args, **kwargs):
        
        data = request.data
        comment = self.get_object()
        
        if kwargs.get('is_original') == True:
            serializer = OriginalCommentSerializer(comment, data=data)
        else:
            serializer = ChildCommentSerializer(comment, data=data)
        
        if serializer.is_valid():
            
            if kwargs.get('is_original') == True:
                if data.get('post_uuid') != None or data.get('owner_uuid') != None:
                    data = {
                        'message': 'post_uuid and owner_uuid must be None'
                    }
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(data=data, status=status_code)
                
            elif kwargs.get('is_original') == False:
                if data.get('commentfeed_uuid') != None or data.get('owner_uuid') != None:
                    data = {
                        'message': 'commentfeed_uuid and owner_uuid must be None'
                    }
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(data=data, status=status_code)
                
            serializer.save()
            status_code = status.HTTP_200_OK
            return Response(data=serializer.data, status=status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            data = {
                'message': self.get_invalid_message()
            }
            return Response(data=data, status=status_code)
    
    def delete(self, request, *args, **kwargs):
        
        comment = self.get_object()
        comment.delete()
        status_code = status.HTTP_200_OK
        return Response(data=None, status=status_code)