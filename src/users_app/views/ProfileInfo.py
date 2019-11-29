from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from users_app.models import Sub

from bloggit_project.utils.permissions import SessionSubOnly

class ProfileInfo(APIView):
    
    permission_classes = (SessionSubOnly,)
    
    def get_queryset(self):
        uuid = self.kwargs.get('sub_uuid')
        sub = Sub.objects.get()
        self.check_object_permissions(self.request, sub)
        return sub
    
    def get(self):
        session_sub = self.get_queryset()
        data = {
            'email': session_sub.user.email,
            'username': session_sub.user.username,
            'communities': session_sub.get_communities_as_list,
            'cake_day': session_sub.get_cake_day,
            'profile_pic_url': session_sub.get_profile_pic_url
        }
        
        return Response(data=data, status=HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        #this will only update the password
        new_password = request.data.get('password')
        confirmation_password = request.data.get('confirmation_password')
        if new_password == confirmation_password:
            request.user.password = new_password
            request.user.save()
            return Response(data=None, status=HTTP_200_OK)
        else:
            return Response(data=None, status=HTTP_400_BAD_REQUEST)