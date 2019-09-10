from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from posts_app.models import Post
from posts_app.serializers.PostSerializer import PostSerializer

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication
from bloggit_project.utils.pagination import CustomPagination

from taggit.models import Tag



class PostsByCommunity(APIView):
    '''return posts related to a specific community(tag)'''

    serializer = PostSerializer
    authentication_classes = (CustomJSONWebTokenAuthentication,)
    paginator = CustomPagination()

    def check_if_subscribed(self):
        slug = self.kwargs['community_slug']

        if self.request.user.is_authenticated:
            session_sub = Sub.objects.get(user=self.request.user)
            if slug in session_sub.communities.as_list:
                return True
            else:
                return False
        
        elif self.request.user.is_anonymous:
            return None

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
            return Post.objects.filter(communities=community).order_by('-id')[0:250]
    
    def get_serializer_context(self):

        if self.request.user.is_authenticated:
            #theres should always be a sub per user
            session_sub = Sub.objects.get(user=self.request.user)
            return {'session_sub': session_sub}
        
        elif self.request.user.is_anonymous:
            return None
    
    def get(self, request, *args, **kwargs):
        '''override list method from ListAPIView'''

        queryset = self.get_queryset()
        context = self.get_serializer_context()
        results = self.paginator.paginate_queryset(queryset, request)
        posts = self.serializer(results, context=context, many=True).data
        
        data = self.paginator.get_paginated_data(posts)
        data['subscribed'] = self.check_if_subscribed()
        data['authenticated'] = request.user.is_authenticated
        status_code = status.HTTP_200_OK

        return Response(data=data, status=status_code)