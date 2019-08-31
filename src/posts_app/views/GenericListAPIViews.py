from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from posts_app.models import Post
from posts_app.serializers.PostSerializer import PostSerializer

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication
from bloggit_project.utils.pagination import CustomPagination

from taggit.models import Tag

from datetime import date

import json


class GenericListAPIView(ListAPIView):
    '''provide a base view that can be inherited'''
    
    serializer = PostSerializer
    authentication_classes = (CustomJSONWebTokenAuthentication,)
    paginator = CustomPagination()
    
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


class HomeView(GenericListAPIView):
    '''retrieve first 500 posts'''
    
    queryset = Post.objects.order_by('-id')[0:500]


class PopularInCommunity(GenericListAPIView):
    '''retrieve most popular posts of a given community'''
    
    today = date.today()
    
    def get_queryset(self):
        slug = self.kwargs['community_slug']
        community = Tag.objects.get(slug=slug)
        
        return Post.objects.filter(communities=community,
                                   date_posted__year=self.today.year,
                                   date_posted__month=self.today.month,
                                   date_posted__day=self.today.day).order_by('likes')