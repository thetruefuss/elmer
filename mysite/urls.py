"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from rest_framework_jwt.views import (
    obtain_jwt_token, refresh_jwt_token, verify_jwt_token,
)

import boards.views as boards_views
import comments.views as comments_views
import notifications.views as notifications_views
import reports.views as reports_views
import search.views as search_views
import subjects.views as subjects_views
import users.views as users_views
from subjects.sitemaps import SubjectSitemap

sitemaps = {
    'subjects': SubjectSitemap,
}

urlpatterns = [
    re_path(r'^$',subjects_views.HomePageView.as_view(), name='home'),
    re_path(r'^trending/$',subjects_views.TrendingPageView.as_view(), name='trending'),
    re_path(r'^s/(?P<board>[-\w]+)/(?P<subject>[-\w]+)/$',
        subjects_views.subject_detail,
        name='subject_detail'),
    re_path(r'^b/$',boards_views.BoardsPageView.as_view(), name='view_all_boards'),
    re_path(r'^b/(?P<board>[-\w]+)/$',
        boards_views.BoardPageView.as_view(),
        name='board'),
    re_path(r'^b/ban_user/(?P<board>[-\w]+)/(?P<user_id>\d+)/$',
        boards_views.ban_user,
        name='ban_user'),
    re_path(r'^b/(?P<board>[-\w]+)/edit_board_cover/$',
        boards_views.edit_board_cover,
        name='edit_board_cover'),
    re_path(r'^b/(?P<board>[-\w]+)/subscription/$',
        boards_views.subscribe,
        name='subscribe'),
    re_path(r'^b/(?P<subject>[-\w]+)/like/$',
        subjects_views.like_subject,
        name='like'),
    re_path(r'^load_new_comments/$', comments_views.load_new_comments, name='load_new_comments'),

    re_path(r'^u/(?P<username>[\w.@+-]+)/subscriptions/$', boards_views.UserSubscriptionListView.as_view(),
        name='user_subscription_list'),
    re_path(r'^u/(?P<username>[\w.@+-]+)/boards/$', boards_views.UserCreatedBoardsPageView.as_view(),
        name='user_created_boards'),
    re_path(r'^new_post/$',subjects_views.new_subject, name='new_subject'),
    re_path(r'^delete_post/(?P<subject>[-\w]+)/$',subjects_views.delete_subject, name='delete_subject'),
    re_path(r'^edit_subject/(?P<subject>[-\w]+)/$', subjects_views.edit_subject, name='edit_subject'),
    re_path(r'^delete_comment/(?P<pk>\d+)/$', comments_views.delete_comment, name='delete_comment'),
    re_path(r'^new_board/$',boards_views.new_board, name='new_board'),

    # user profiles
    re_path(r'^u/$', users_views.UsersPageView.as_view(), name='view_all_users'),
    re_path(r'^u/following/$', users_views.FollowingPageView.as_view(), name='view_following'),
    re_path(r'^u/followers/$', users_views.FollowersPageView.as_view(), name='view_all_followers'),
    re_path(r'^u/(?P<username>[\w.@+-]+)/$', users_views.UserProfilePageView.as_view(), name='user_profile'),
    re_path(r'^u/follow_user/(?P<user_id>\d+)/$',
        users_views.follow_user,
        name='follow_user'),
    re_path(r'^u/send_message_request/(?P<user_id>\d+)/$',
        users_views.send_message_request,
        name='send_message_request'),
    re_path(r'^u/accept_message_request/(?P<user_id>\d+)/$',
        users_views.accept_message_request,
        name='accept_message_request'),
    re_path(r'^u/block_spammer/(?P<user_id>\d+)/$',
        users_views.block_spammer,
        name='block_spammer'),
    re_path(r'^u/friends/all/$', users_views.all_friends, name='all_friends'),
    re_path(r'^u/friends/requests/$', users_views.all_message_requests, name='all_message_requests'),
    re_path(r'^activities/$', notifications_views.ActivitiesPageView.as_view(), name='activities'),
    re_path(r'^activities/check/$', notifications_views.check_activities, name='check_activities'),

    # login / logout urls
    re_path(r'^login/$',
            auth_views.LoginView.as_view(extra_context={'form_filling': True}),
            name='login'),
    re_path(r'^logout/$',
            auth_views.LogoutView.as_view(next_page="/"),
            name='logout'),
    re_path(r'^logout-then-login/$',
            auth_views.logout_then_login,
            name='logout_then_login'),

    # password change re_paths
    re_path(r'^password_change/$',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'),
    re_path(r'^password-change/done/$',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'),

    # password reset
    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # user registration
    re_path(r'^signup/$',
        users_views.register_user,
        name='signup'),

    # verify username availability in database via ajax request
    re_path(r'^signup/check_username/$', users_views.check_username, name='check_username'),

    # profile edit
    re_path(r'^profile_edit/$', users_views.profile_edit,
        name='profile_edit'),
    re_path(r'^picture_change/$', users_views.change_picture,
        name='picture_change'),

    # search
    re_path(r'^search/$',search_views.search, name='search'),
    re_path(r'^board_search/(?P<board_slug>[-\w]+)/$',search_views.search, name='board_search'),

    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),

    # report
    re_path(r'^banned_users/(?P<board>[-\w]+)/$',
        boards_views.banned_users,
        name='banned_users'),
    re_path(r'^report_subject/(?P<subject>[-\w]+)/$',
        reports_views.report_subject,
        name='report_subject'),
    re_path(r'^report_comment/(?P<pk>\d+)/$',
        reports_views.report_comment,
        name='report_comment'),
    re_path(r'^show_reports/(?P<board>[-\w]+)/$',
        reports_views.show_reports,
        name='show_reports'),
    re_path(r'^deactivate_subject/(?P<subject>[-\w]+)/$',
        subjects_views.deactivate_subject,
        name='deactivate_subject'),
    re_path(r'^deactivate_comment/(?P<pk>\d+)/$',
        comments_views.deactivate_comment,
        name='deactivate_comment'),
    re_path(r'^messages/', include('messenger.urls')),

    # api urls
    re_path(r'^api/auth/token/obtain/', obtain_jwt_token),
    re_path(r'^api/auth/token/refresh/', refresh_jwt_token),
    re_path(r'^api/auth/token/verify/', verify_jwt_token),
    re_path(r'^api/frontboard/', include('subjects.api.urls')),
    re_path(r'^api/frontboard/', include('boards.api.urls')),
    re_path(r'^api/frontboard/', include('reports.api.urls')),
    re_path(r'^api/frontboard/', include('comments.api.urls')),
    re_path(r'^api/users/', include('users.api.urls')),
    re_path(r'^api/users/', include('notifications.api.urls')),
    re_path(r'^api/messages/', include('messenger.api.urls')),
]

if True:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

# flatpages urls
urlpatterns.append(re_path(r'^', include('django.contrib.flatpages.urls')))
