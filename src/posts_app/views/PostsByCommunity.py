from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response

from posts_app.models import Post
from posts_app.serializers.PostSerializer import PostSerializer

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication
from bloggit_project.utils.pagination import CustomPagination
from bloggit_project.utils.permissions import ReadOnly

from taggit.models import Tag


class PostsByCommunity(ListAPIView):
    '''return posts related to a specific community(tag)'''

    serializer = PostSerializer
    authentication_classes = (CustomJSONWebTokenAuthentication,)
    paginator = CustomPagination()
    permission_classes = (ReadOnly,)
    people_in_community = None

    def get_queryset(self):
        #first get the community
        slug = self.kwargs['community_slug']

        try:
            community = Tag.objects.get(slug=slug)
        
        except Tag.DoesNotExist:
            #if community does not exist send a 404 response
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        
        else:
            #if community does exists send a queryset of posts that
            #have community in obj.communities
            self.people_in_community = Sub.objects.filter(communities=community).count()
            return Post.objects.filter(communities=community).order_by('-id')[0:250]
    
    def get_serializer_context(self):

        if self.request.user.is_authenticated:
            #theres should always be a sub per user
            session_sub = Sub.objects.get(user=self.request.user)
            return {'session_sub': session_sub}
        
        elif self.request.user.is_anonymous:
            return None
    
    def list(self, request, *args, **kwargs):
        '''override list method from ListAPIView'''

        queryset = self.get_queryset()
        context = self.get_serializer_context()
        results = self.paginator.paginate_queryset(queryset, request)
        posts = self.serializer(results, context=context, many=True).data
        
        data = self.paginator.get_paginated_data(posts, request)
        if self.people_in_community != None:
            data['people_in_community'] = self.people_in_community
        status_code = status.HTTP_200_OK

        return Response(data=data, status=status_code)