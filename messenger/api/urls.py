#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
    ContactsListAPIView,
    MessageCreateAPIView,
    MessageListAPIView,
)

urlpatterns = [
    url(r'^contacts/$', ContactsListAPIView.as_view(), name='list_contacts'),
    url(r'^chat/$', MessageListAPIView.as_view(), name='list_messages'),
    url(r'^send/$', MessageCreateAPIView.as_view(), name='create_message'),
]
