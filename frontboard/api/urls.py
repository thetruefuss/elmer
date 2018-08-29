from django.conf.urls import url

from .views import (ActiveThreadsList, BoardListCreateAPIView,
                    BoardRetrieveUpdateDestroyAPIView, CommentDestroyAPIView,
                    CommentListCreateAPIView, GetSubscribedBoards,
                    StarSubjectView, SubjectListCreateAPIView,
                    SubjectRetrieveUpdateDestroyAPIView, SubscribeBoardView,
                    TrendingBoardsList, ReportListCreateAPIView)

urlpatterns = [
    url(r'^subjects/$', SubjectListCreateAPIView.as_view(), name='list_or_create_subjects'),
    url(r'^subjects/(?P<slug>[-\w]+)/$',
        SubjectRetrieveUpdateDestroyAPIView.as_view(),
        name='retrieve_or_update_or_destroy_subjects'),

    url(r'^boards/$', BoardListCreateAPIView.as_view(), name='list_or_create_boards'),
    url(r'^boards/(?P<slug>[-\w]+)/$',
        BoardRetrieveUpdateDestroyAPIView.as_view(),
        name='retrieve_or_update_or_destroy_boards'),

    url(r'^comments/$', CommentListCreateAPIView.as_view(), name='list_or_create_comments'),
    url(r'^comments/(?P<id>\d+)/$', CommentDestroyAPIView.as_view(), name='destroy_comments'),

    url(r'^reports/$', ReportListCreateAPIView.as_view(), name='list_or_create_reports'),

    url(r'^actions/star/$', StarSubjectView.as_view()),
    url(r'^actions/subscribe/$', SubscribeBoardView.as_view()),

    url(r'^user_active_threads/$', ActiveThreadsList.as_view()),
    url(r'^top_five_boards/$', TrendingBoardsList.as_view()),
    url(r'^user_subscribed_boards/$', GetSubscribedBoards.as_view()),
]
