from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
)

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to to validate or save
        # just want serializer to turn 'User' into something
        # that can be JSONified and sent to client
        serializer = self.serializer_class(request.user)

        return Response(serializer.data,
        status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class RegistrationAPIView(APIView):
    #Allow user to hit this endpoint regardless
    #of authenticaiton
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer, )
    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,
        status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = (UserJSONRenderer, )

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data,
        status=status.HTTP_200_OK)
