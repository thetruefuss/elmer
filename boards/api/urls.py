#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import (
    BoardListCreateAPIView,
    BoardRetrieveUpdateDestroyAPIView,
    GetSubscribedBoards,
    SubscribeBoardView,
    TrendingBoardsList,
)

urlpatterns = [
    url(r'^boards/$', BoardListCreateAPIView.as_view(), name='list_or_create_boards'),
    url(r'^boards/(?P<slug>[-\w]+)/$',
        BoardRetrieveUpdateDestroyAPIView.as_view(),
        name='retrieve_or_update_or_destroy_boards'),
    url(r'^actions/subscribe/$', SubscribeBoardView.as_view()),
    url(r'^top_five_boards/$', TrendingBoardsList.as_view()),
    url(r'^user_subscribed_boards/$', GetSubscribedBoards.as_view()),
]
