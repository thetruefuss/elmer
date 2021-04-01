#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import CommentDestroyAPIView, CommentListCreateAPIView

urlpatterns = [
    url(r'^comments/$', CommentListCreateAPIView.as_view(), name='list_or_create_comments'),
    url(r'^comments/(?P<id>\d+)/$', CommentDestroyAPIView.as_view(), name='destroy_comments'),
]
