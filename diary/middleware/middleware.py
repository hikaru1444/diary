import logging
import threading

local = threading.local()


class CustomAttrMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user:
            setattr(local, 'user', request.user.username)
        else:
            setattr(local, 'user', None)
        response = self.get_response(request)
        return response


class CustomAttrFilter(logging.Filter):
    def filter(self, record):
        record.user = getattr(local, 'user', None)
        return True
