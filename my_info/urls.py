#-*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'my_info.views.info_page', name='home'),
    url(r'^requests/$', 'my_info.views.logged_requests_page', name='logged_requests_page'),
    url(r'^edit_contacts/$', 'my_info.views.edit_contacts', name='edit_contacts'),
    url(r'^edit_contacts_inline/$', 'my_info.views.inline_contacts_edit', name='inline_contacts_edit'),
)
