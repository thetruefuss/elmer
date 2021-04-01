#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import NotificationListAPIView

urlpatterns = [
    url(r'^notifications/$', NotificationListAPIView.as_view(), name='list_notifications'),
]
