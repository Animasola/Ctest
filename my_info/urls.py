#-*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'my_info.views.info_page', name='home'),
)
