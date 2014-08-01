#-*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'my_info.views.info_page', name='home'),
    url(r'^requests/$', 'my_info.views.logged_requests_page', name='logged_requests_page'),
)
