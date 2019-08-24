#profile data for sub model views

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from posts_app.models import Post, Comment
from posts_app.serializers.PostSerializer import PostSerializer
from posts_app.serializers.CommentSerializer import CommentSerializer

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication

import json

class ProfileData(APIView):
    '''return all posts, comments and communities'''
    '''a sub has made so far, also provide its profile picture'''

    authentication_classes = (CustomJSONWebTokenAuthentication,)

    def get(self, request, *args, **kwargs):

        uuid = kwargs['sub_uuid']
        #there is always supposed to be a sub object per user
        session_sub = Sub.objects.get(uuid=uuid)
        posts_query = Post.objects.filter(owner=session_sub).order_by('-id')
        comments_query = Comment.objects.filter(owner=session_sub).order_by('-id')
        context = {'session_sub': session_sub}

        posts = PostSerializer(posts_queryset, context=context, many=True).data
        comments = CommentSerializer(comments_queryset, context=context, many=True).data
        communities = session_sub.get_communities_as_list

        json_data = json.dumps({
            'username': session_sub.get_username,
            'profile_picture': session_sub.get_profile_pic,
            'cake_day': session_sub.get_cake_day,
            'uuid': session_sub.get_uuid_as_string,
            'posts': posts,
            'comments': comments,
            'communities': communities,
            'authenticated': request.user.is_authenticated
        })
        
        status_code = status.HTTP_200_OK

        return Response(data=json_data, status=status_code, content_type='json')