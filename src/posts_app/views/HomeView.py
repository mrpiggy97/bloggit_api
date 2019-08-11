#home view

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

from posts_app.models import Post
from posts_app.serializers.PostSerializer import PostSerializer

from users_app.models import Sub

import json


class HomeView(ListAPIView):
    '''return most recent posts'''
    
    queryset = Post.objects.order_by('-id')[0:250]
    serializer = PostSerializer
    paginator = PageNumberPagination()
    
    def get_serializer_context(self):
        
        if self.request.user.is_authenticated:
            session_sub = Sub.objects.get(user=self.request.user)
            return {'session_sub': session_sub}
        
        else:
            return None
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        context = self.get_serializer_context()
        results = self.paginator.paginate_queryset(queryset, request)
        posts = self.serializer(results, context=context, many=True).data
        
        data = self.paginator.get_paginated_data(posts)
        json_data = json.dumps(data)
        status_code = status.HTTP_200_OK
        
        return Response(data=json_data, status=status_code, content_type='json')