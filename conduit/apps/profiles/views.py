from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer


class ProfileRetrieveAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny, )
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = (ProfileSerializer)

    def retrieve(self, request, username, *args, **kwargs):
        try:
            # Use 'select_related' to avoid unneccessary database calls
            profile = Profile.objects.select_related('user').get(
                user__username=username
            )
        except Profile.DoesNotExist:
            raise

        serilizer = self.serilizer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)
