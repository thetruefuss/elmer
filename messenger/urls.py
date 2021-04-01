#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.inbox, name='inbox'),
    url(r'^send/$', views.send, name='send_message'),
    url(r'^delete/$', views.delete, name='delete_message'),
    url(r'^check/$', views.check, name='check_message'),
    url(r'^load_new_messages/$', views.load_new_messages, name='load_new_messages'),
    url(r'^load_last_twenty_messages/$', views.load_last_twenty_messages, name='load_last_twenty_messages'),
    url(r'^(?P<username>[^/]+)/$', views.messages, name='messages'),
]
