#-*- coding:utf-8 -*-
from django.conf import settings


def django_settings(request):
    return {'django_settings': settings}
