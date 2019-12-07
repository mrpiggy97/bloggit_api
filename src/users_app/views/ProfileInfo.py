from django.contrib.auth import password_validation
from django.core import exceptions

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from users_app.models import Sub


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_info(request):
    session_sub = Sub.objects.get(user=request.user)
    status_code = status.HTTP_200_OK
    data = {
        'email': session_sub.user.email,
        'username': session_sub.user.username,
        'communities': session_sub.get_communities_as_list,
        'cake_day': session_sub.get_cake_day,
        'profile_pic_url': session_sub.get_profile_pic_url
    }
    
    return Response(data=data, status=status_code)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def change_password(request):
    '''change the password of the incoming user'''
    data = request.data
    if data.get('newPassword') != data.get('confirmationPassword'):
        status_code = status.HTTP_400_BAD_REQUEST
        d = {
            'message': 'the passwords did not match'
        }
        return Response(data=d, status=status_code)
    
    elif data.get('newPassword') == data.get('confirmationPassword'):
        #to do, apply password validation before changing users password
        new_password = data.get('newPassword')
        try:
            password_validation.validate_password(new_password, user=request.user)
        except exceptions.ValidationError as errors:
            d = {
                'errors': errors.messages
            }
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(data=d, status=status_code)
        else:
            
            status_code = status.HTTP_200_OK
            request.user.password = new_password
            request.user.save()
            return Response(data=None, status=status_code)