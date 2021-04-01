#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
    ActiveThreadsList,
    StarSubjectView,
    SubjectListCreateAPIView,
    SubjectRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    url(r'^subjects/$', SubjectListCreateAPIView.as_view(), name='list_or_create_subjects'),
    url(r'^subjects/(?P<slug>[-\w]+)/$',
        SubjectRetrieveUpdateDestroyAPIView.as_view(),
        name='retrieve_or_update_or_destroy_subjects'),
    url(r'^actions/star/$', StarSubjectView.as_view()),
    url(r'^user_active_threads/$', ActiveThreadsList.as_view()),
]
