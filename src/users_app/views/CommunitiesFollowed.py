#add and remove communities from Sub.communities

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users_app.models import Sub

from taggit.models import Tag


class CommunitiesFollowed(APIView):
    '''endpoint to add and remove communities from Sub.communities'''

    def get_object(self):

        slug = self.kwargs['community_slug']
        
        try:
            community = Tag.objects.get(slug=slug)
        
        except Tag.DoesNotExist:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        
        else:
            return community

    def put(self, request, *args, **kwargs):
        '''add community to sub.communities'''

        session_sub = Sub.objects.get(user=request.user)
        community = self.get_object()
        session_sub.communities.add(community)
        return Response(data=None, status=status.HTTP_202_ACCEPTED)
    
    def delete(self, request, *args, **kwargs):
        '''remove community from sub.communities'''

        session_sub = Sub.objects.get(user=request.user)
        community = self.get_object()
        session_sub.communities.remove(community)
        return Response(data=None, status=status.HTTP_202_ACCEPTED)