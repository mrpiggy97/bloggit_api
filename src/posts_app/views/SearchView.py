#return a query based on request.data
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from posts_app.models import Post
from posts_app.serializers.PostSerializer import PostSerializer

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication
from bloggit_project.utils.pagination import CustomPagination
from bloggit_project.utils.search_for_posts import search_for_posts
from bloggit_project.utils.permissions import ReadOnly

from taggit.models import Tag

class SearchView(ListAPIView):
    '''return a query based on data sent by request'''

    authentication_classes = (CustomJSONWebTokenAuthentication,)
    serializer = PostSerializer
    paginator = CustomPagination()
    permission_classes = (ReadOnly,)
    
    def get_queryset(self):
        queryset = search_for_posts(self.kwargs.get('query'))
        return queryset
    
    def get_serializer_context(self):

        if self.request.user.is_authenticated:
            #there should always be a sub object per user
            session_sub = Sub.objects.get(user=self.request.user)
            return {'session_sub': session_sub}
        
        elif self.request.user.is_anonymous:
            return None
    
    def list(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        context = self.get_serializer_context()

        results = self.paginator.paginate_queryset(queryset, request)
        posts = self.serializer(results, context=context, many=True).data
        data = self.paginator.get_paginated_data(posts, request)
        status_code = status.HTTP_200_OK
        return Response(data=data, status=status_code)