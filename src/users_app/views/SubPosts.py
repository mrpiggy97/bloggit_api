from rest_framework.generics import ListAPIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from posts_app.models import Post
from posts_app.serializers.PostSerializer import PostSerializer

from users_app.models import Sub

from bloggit_project.utils.pagination import CustomPagination
from bloggit_project.utils.authentication import CustomJSONWebTokenAuthentication
from bloggit_project.utils.permissions import ReadOrOwnerOnly

class SubPosts(ListAPIView):
    serializer = PostSerializer
    authentication_classes = (CustomJSONWebTokenAuthentication,)
    permission_classes = (ReadOrOwnerOnly,)
    paginator = CustomPagination()
    
    def get_queryset(self):
        uuid = self.kwargs.get('sub_uuid')
        sub = Sub.objects.get(uuid=uuid)
        return Post.objects.filter(owner=sub).order_by('-id')
    
    def get_serializer_context(self):
        if self.request.user.is_authenticated:
            uuid = self.kwargs.get('sub_uuid')
            session_sub = Sub.objects.get(uuid=uuid)
            return {'session_sub': session_sub}
        else:
            return None
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        context = self.get_serializer_context()
        results = self.paginator.paginate_queryset(queryset, request)
        posts = self.serializer(results, context=context, many=True).data
        data = self.paginator.get_paginated_data(posts, request)
        return Response(data=data, status=HTTP_200_OK)