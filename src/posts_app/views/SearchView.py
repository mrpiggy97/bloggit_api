#return a query based on request.data
from django.db.models import Q

from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from posts_app.models import Post
from posts_app.serializers.PostSerializer import PostSerializer

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication

from taggit.models import Tag

import json


class SearchView(ListAPIView):
    '''return a query based on data sent by request'''

    authentication_classes = (CustomJSONWebTokenAuthentication,)
    serializer = PostSerializer

    def get_queryset(self):
        query = self.kwargs['query']
        #separate every word in query by space
        queryList = list(query.split(" "))
        communities = {}
        #communities whose name are found in query
        relevantCommunities = []
        posts = []

        #filter communities based on every word in queryList
        for word in queryList:
            comms = Tag.objects.filter(Q(slug__icontains=word))
            communities[word] = comms
        #loop through every communityList in communities
        for communityList in communities.values():
            #loop through every community in comunityList
            for community in communityList:
                #if the name of current community is found in query and has yet
                #to be appended to relevantCommunities append it
                if community.name in query and community not in relevantCommunities:
                    relevantCommunities.append(community)
        
        #loop through every community relevant to query (relevantCommunities)
        #make a query with every community and append every post found in that
        #query if post not in posts
        for community in relevantCommunities:
            postsQuery = Post.objects.filter(communities=community).order_by('-id')
            
            for post in postsQuery:
                if post not in posts:
                    posts.append(post)
        
        return posts
    
    def get_serializer_context(self):

        if self.request.user.is_authenticated:
            #there should always be a sub object per user
            session_sub = Sub.objects.get(user=self.request.user)
            return {'session_sub': session_sub}
        
        elif self.request.user.is_anonymous:
            return None
    
    def list(self, request, *args, **kwargs):

        posts = self.get_queryset()
        context = self.get_serializer_context()

        data = self.serializer(posts, context=context, many=True).data
        json_data = json.dumps(data)

        return Response(data=json_data, status=status.HTTP_200_OK, content_type='json')