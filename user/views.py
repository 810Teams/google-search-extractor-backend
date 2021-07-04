"""
    User Application Views
    user/views.py
"""

from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ User view set """
    queryset = get_user_model().objects.all()
    http_method_names = ('get', 'head', 'options')
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer


class MyUserView(generics.ListAPIView):
    """ My user view """
    queryset = get_user_model().objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        """ Retrieve own user """
        user = self.get_queryset().get(pk=request.user.id)
        serializer = self.get_serializer(user, many=False)

        return Response(serializer.data)


class LoginAPIView(ObtainAuthToken):
    """ Login API view """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
