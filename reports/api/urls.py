#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import ReportListCreateAPIView

urlpatterns = [
    url(r'^reports/$', ReportListCreateAPIView.as_view(), name='list_or_create_reports'),
]
