from conduit.apps.core.renderers import ConduitJSONRenderer

class UserJSONRenderer(ConduitJSONRenderer):
    object_label='user'

    def render(self, data, media_type=None, renderer_context=None):

        #Byte objects don't serialize well, so we decode token
        token = data.get('token', None)

        #Place decoded token back in place of its coded brethren
        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        # Once token is decoded, simply use the super(ConduitJSONRenderer)
        # render method on the data
        return super(UserJSONRenderer, self).render(data)
#
