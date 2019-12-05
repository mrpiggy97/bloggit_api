from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.generics import ListAPIView

from posts_app.models import Post, Comment
from posts_app.serializers.CommentSerializer import (OriginalCommentSerializer,
                                                     ChildCommentSerializer)

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication
from bloggit_project.utils.pagination import CustomPagination
from bloggit_project.utils.permissions import  ReadOnly

from collections import OrderedDict
class SubComments(ListAPIView):
    
    authentication_classes = (CustomJSONWebTokenAuthentication,)
    permission_classes = (ReadOnly,)
    og_serializer = OriginalCommentSerializer
    ch_serializer = ChildCommentSerializer
    paginator = CustomPagination()
    
    def get_serializer_context(self):
        
        if self.request.user.is_authenticated:
            session_sub = Sub.objects.get(user=self.request.user)
            return {'session_sub': session_sub}
        else:
            return None
    
    def get_original_comments(self):
        uuid = self.kwargs.get('sub_uuid')
        owner = Sub.objects.get(uuid=uuid)
        context = self.get_serializer_context()
        queryset = Comment.objects.filter(owner=owner, is_original=True)
        return self.og_serializer(queryset, context=context, many=True).data
    
    def get_child_comments(self):
        uuid = self.kwargs.get('sub_uuid')
        owner = Sub.objects.get(uuid=uuid)
        context = self.get_serializer_context()
        queryset = Comment.objects.filter(owner=owner, is_original=False)
        return self.ch_serializer(queryset, context=context, many=True).data
    
    def get_queryset(self):
        uuid = self.kwargs.get('sub_uuid')
        sub = Sub.objects.get(uuid=uuid)
        return Comment.objects.filter(owner=sub).order_by('-id')
        
    def list(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        queryset = self.get_queryset()
        results = self.paginator.paginate_queryset(queryset, request)
        
        original_comments = list(filter(lambda Comment:Comment.is_original == False,
                                        results))
        child_comments = list(filter(lambda Comment:Comment.is_original == False,
                                     results))
        
        serialized_original_comments = self.og_serializer(original_comments,
                                                          context=context,
                                                          many=True).data
        serialized_child_comments = self.ch_serializer(child_comments,
                                                       context=context,
                                                       many=True).data
        comments = serialized_original_comments + serialized_child_comments
        comments.sort(key=lambda i:i.get('id'), reverse=True)
        data = self.paginator.get_paginated_data(comments, request)
        return Response(data=data, status=HTTP_200_OK)