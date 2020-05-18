'''filter Post objects by community'''

from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from taggit.models import Tag

from posts_app.models import Post
from posts_app.serializers.PostSerializer import PostSerializer

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication
from bloggit_project.utils.pagination import CustomPagination
from bloggit_project.utils.permissions import ReadOnly

class PostsByCommunity(ListAPIView):
    '''return posts related to a specific community(tag)'''

    serializer = PostSerializer
    authentication_classes = (CustomJSONWebTokenAuthentication,)
    paginator = CustomPagination()
    permission_classes = (ReadOnly,)
    people_in_community = None
    posts_in_community = None

    def get_queryset(self):
        '''first get the community'''
        slug = self.kwargs['community_slug']

        try:
            community = Tag.objects.get(slug=slug)
        
        except Tag.DoesNotExist:
            #if community does not exist send a 404 response
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        
        else:
            #if community does exists send a queryset of posts that
            #have community in obj.communities
            posts = Post.objects.filter(communities=community).order_by('-id')[0:250]
            if self.kwargs.get('get_community_info'):
                self.posts_in_community = posts.count()
                subs = Sub.objects.filter(communities=community)
                self.people_in_community = subs.count()
            return posts
    
    def get_serializer_context(self):
        '''return context to be used by the serializer'''
        if self.request.user.is_authenticated:
            #theres should always be a sub per user
            session_sub = Sub.objects.get(user=self.request.user)
            return {'session_sub': session_sub}
        return None
    
    def list(self, request, *args, **kwargs):
        '''override list method from ListAPIView'''

        queryset = self.get_queryset()
        context = self.get_serializer_context()
        results = self.paginator.paginate_queryset(queryset, request)
        posts = self.serializer(results, context=context, many=True).data
        
        data = self.paginator.get_paginated_data(posts, request)
        if kwargs.get('get_community_info'):
            data['people_in_community'] = self.people_in_community
            data['posts_in_community'] = self.posts_in_community
        status_code = status.HTTP_200_OK

        return Response(data=data, status=status_code)