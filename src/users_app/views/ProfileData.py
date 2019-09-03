#profile data for sub model views

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from posts_app.models import Post, Comment
from posts_app.serializers.PostSerializer import PostSerializer
from posts_app.serializers.CommentSerializer import CommentSerializer

from users_app.models import Sub

from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication

class ProfileData(APIView):
    '''return all posts, comments and communities'''
    '''a sub has made so far, also provide its profile picture'''

    authentication_classes = (CustomJSONWebTokenAuthentication,)
    
    def get_serializer_context(self):
        
        if self.request.user.is_authenticated:
            session_sub = Sub.objects.get(user=self.request.user)
            return  {'session_sub': session_sub}
        else:
            return None

    def get(self, request, *args, **kwargs):

        uuid = kwargs['sub_uuid']
        #there is always supposed to be a sub object per user
        profile_sub = Sub.objects.get(uuid=uuid)
        posts_query = Post.objects.filter(owner=profile_sub).order_by('-id')
        comments_query = Comment.objects.filter(owner=profile_sub).order_by('-id')
        context = self.get_serializer_context()

        posts = PostSerializer(posts_query, context=context, many=True).data
        comments = CommentSerializer(comments_query, context=context, many=True).data
        communities = profile_sub.get_communities_as_list

        data = {
            'username': profile_sub.get_username,
            'profile_picture': profile_sub.get_profile_pic,
            'cake_day': profile_sub.get_cake_day,
            'uuid': profile_sub.get_uuid_as_string,
            'communities': communities,
            'authenticated': request.user.is_authenticated,
            'posts': posts,
            'comments': comments,
        }
        
        status_code = status.HTTP_200_OK

        return Response(data=data, status=status_code)