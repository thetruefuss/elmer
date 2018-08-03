from django.conf.urls import url

from .views import (BoardCreateAPIView, BoardDestroyAPIView, BoardListAPIView,
                    BoardRetrieveAPIView, BoardUpdateAPIView, TrendingBoardsList,
                    SubjectCreateAPIView, SubjectDestroyAPIView, ActiveThreadsList,
                    SubjectListAPIView, SubjectRetrieveAPIView, GetSubscribedBoards,
                    SubjectUpdateAPIView, CommentListAPIView, CommentCreateAPIView,
                    StarSubjectView)

urlpatterns = [
    url(r'^subjects/$', SubjectListAPIView.as_view(), name='subjects_list'),
    url(r'^subjects/active_threads/$', ActiveThreadsList.as_view(), name='active_threads'),
    url(r'^subjects/star/$', StarSubjectView.as_view(), name='star_subject'),
    url(r'^subjects/create/$', SubjectCreateAPIView.as_view(), name='subjects_create'),
    url(r'^subjects/(?P<slug>[-\w]+)/$', SubjectRetrieveAPIView.as_view(), name='subjects_retrieve'),
    url(r'^subjects/(?P<slug>[-\w]+)/edit/$', SubjectUpdateAPIView.as_view(), name='subjects_update'),
    url(r'^subjects/(?P<slug>[-\w]+)/delete/$', SubjectDestroyAPIView.as_view(), name='subjects_delete'),

    url(r'^boards/$', BoardListAPIView.as_view(), name='boards_list'),
    url(r'^boards/trending/$', TrendingBoardsList.as_view(), name='boards_trending'),
    url(r'^boards/user_subscribed/$', GetSubscribedBoards.as_view(), name='boards_users'),
    url(r'^boards/create/$', BoardCreateAPIView.as_view(), name='boards_create'),
    url(r'^boards/(?P<slug>[-\w]+)/$', BoardRetrieveAPIView.as_view(), name='boards_retrieve'),
    url(r'^boards/(?P<slug>[-\w]+)/edit/$', BoardUpdateAPIView.as_view(), name='boards_update'),
    url(r'^boards/(?P<slug>[-\w]+)/delete/$', BoardDestroyAPIView.as_view(), name='boards_delete'),

    url(r'^comments/create/$', CommentCreateAPIView.as_view(), name='comments_create'),
    url(r'^comments/(?P<slug>[-\w]+)/$', CommentListAPIView.as_view(), name='comments_list'),
]
