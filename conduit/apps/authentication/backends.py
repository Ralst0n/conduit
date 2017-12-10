import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        """
        The 'authenticate' method is called on every request
        regardless of whether the endpoint requires authentication.

        'authenticate' has two possible return values

        1) 'None' - Return 'None' if don't want to authenticate.
                    i.e. when authentication will fail.
                    i.i.e when request does not include a token in header.

        2) '(user, token)' - returned when user/token combination is successful

                            If neither case is met then there is an error
                            and nothing is returned
                            raise 'AuthenticationFailed' exception for DRF
                            to handle.
        """
        request.user = None

        # auth_header is array with [name of auth header ("Token"),
        #                            JWT to authenticate against]
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # no credentials provided
            # don't bother authenticating
            return None

        elif len(auth_header) > 2:
            # Also invalid, don't authenticate
            return None

        # JWT library can't handle 'byte' type
        # decode 'prefix' & 'token'
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() !=auth_header_prefix:
            # header is not what was expected, don't authenticate
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        Try to authenticate the given credentials.
        return user & token if successful
        else throw an error.
        """

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invalid authentication. Could not decode token'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated'
            raise exception.AuthenticationFailed(msg)

        return (user, token)
