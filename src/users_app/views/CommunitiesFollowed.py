'''add and remove communities from Sub.communities'''

from taggit.models import Tag

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED, HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated

from users_app.models import Sub

class CommunitiesFollowed(APIView):
    '''endpoint to add and remove communities from Sub.communities'''
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        '''get community tag'''
        slug = self.kwargs.get("community_slug")
        
        try:
            community = Tag.objects.get(slug=slug)
        
        except Tag.DoesNotExist:
            return Response(data=None, status=HTTP_404_NOT_FOUND)
        
        else:
            self.check_object_permissions(self.request, community)
            return community

    def put(self, request, *args, **kwargs):
        '''add community to sub.communities'''
        session_sub = Sub.objects.get(user=request.user)
        community = self.get_object()
        session_sub.communities.add(community)
        return Response(data=None, status=HTTP_202_ACCEPTED)
    
    def delete(self, request, *args, **kwargs):
        '''remove community from sub.communities'''
        session_sub = Sub.objects.get(user=request.user)
        community = self.get_object()
        session_sub.communities.remove(community)
        return Response(data=None, status=HTTP_202_ACCEPTED)
