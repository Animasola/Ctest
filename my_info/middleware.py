#-*- coding:utf-8 -*-
from my_info.models import LoggedRequest


class RequestLogger(object):
    def process_request(self, request):
        try:
            LoggedRequest.objects.create(**{
                'ip': request.META['REMOTE_ADDR'],
                'request_type': request.method,
                'url': request.build_absolute_uri(request.path)
            })
        except Exception, e:
            raise Exception("Middleware failed to log request:\n" + str(e))
