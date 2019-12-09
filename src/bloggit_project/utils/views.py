from django.utils.translation import ugettext_lazy as _

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_auth.registration.views import RegisterView

from users_app.models import Sub

from bloggit_project.utils.serializers import CustomPasswordResetSerializer

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
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        Sub.objects.create(user=user)
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)