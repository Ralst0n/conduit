from rest_framework.views import exception_handler

def core_exception_handler(exc, context):

    response = exception_handler(exc, context)
    handlers = {
        'ValidationError': _handle_generic_error
    }

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        # if this requires custom handler,
        # use custom handler
        # otherwise return default handler from above
        return handlers[exception_class](exc, context, response)

    return response

def _handle_generic_error(exc, context, response):
    #take the response generated by DRF & wrap it in the 'error' key
    response.data = {
        'errors': response.data
    }

    return response