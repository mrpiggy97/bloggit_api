from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework_jwt.settings import api_settings

from rest_auth.app_settings import (TokenSerializer, JWTSerializer)
from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView
from rest_auth.utils import jwt_encode

from allauth.account import app_settings as allauth_settings

from users_app.models import Sub

from bloggit_project.utils.serializers import CustomPasswordResetSerializer
from bloggit_project.utils.payload_handler import payload_handler

class CustomPasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = CustomPasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )


class CustomRegisterView(RegisterView):
    '''create sub along with user'''
    #method overriden so a sub can be created when a user is created
    #nothing is deleted or changed, only Sub.object.create was inserted
    def get_response_data(self, user, session_sub):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent.")}

        if getattr(settings, 'REST_USE_JWT', False):
            #overrode method to return what custom payload handler returns
            data = payload_handler(self.token, user=user, session_sub=session_sub)
            return data
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        sub = Sub.objects.create(user=user)
        headers = self.get_success_headers(serializer.data)
        response = self.get_response_data(user, sub)

        return Response(response,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

class CustomLoginView(LoginView):
    '''will override get_response method and login method'''

    def get_response(self):
        
        data = payload_handler(self.token, user=self.user)

        response = Response(data=data, status=status.HTTP_200_OK)
        if api_settings.JWT_AUTH_COOKIE:
            expiration = (datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA)
            response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                self.token,
                                expires=expiration,
                                httponly=True)
        return response