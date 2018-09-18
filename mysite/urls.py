from django.conf import settings
from django.conf.urls import include, url
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
    url(r'^$',subjects_views.HomePageView.as_view(), name='home'),
    url(r'^trending/$',subjects_views.TrendingPageView.as_view(), name='trending'),
    url(r'^s/(?P<board>[-\w]+)/(?P<subject>[-\w]+)/$',
        subjects_views.subject_detail,
        name='subject_detail'),
    url(r'^b/$',boards_views.BoardsPageView.as_view(), name='view_all_boards'),
    url(r'^b/(?P<board>[-\w]+)/$',
        boards_views.BoardPageView.as_view(),
        name='board'),
    url(r'^b/ban_user/(?P<board>[-\w]+)/(?P<user_id>\d+)/$',
        boards_views.ban_user,
        name='ban_user'),
    url(r'^b/(?P<board>[-\w]+)/edit_board_cover/$',
        boards_views.edit_board_cover,
        name='edit_board_cover'),
    url(r'^b/(?P<board>[-\w]+)/subscription/$',
        boards_views.subscribe,
        name='subscribe'),
    url(r'^b/(?P<subject>[-\w]+)/like/$',
        subjects_views.like_subject,
        name='like'),
    url(r'^load_new_comments/$', comments_views.load_new_comments, name='load_new_comments'),

    url(r'^u/(?P<username>[\w.@+-]+)/subscriptions/$', boards_views.UserSubscriptionListView.as_view(),
        name='user_subscription_list'),
    url(r'^u/(?P<username>[\w.@+-]+)/boards/$', boards_views.UserCreatedBoardsPageView.as_view(),
        name='user_created_boards'),
    url(r'^new_post/$',subjects_views.new_subject, name='new_subject'),
    url(r'^delete_post/(?P<subject>[-\w]+)/$',subjects_views.delete_subject, name='delete_subject'),
    url(r'^edit_subject/(?P<subject>[-\w]+)/$', subjects_views.edit_subject, name='edit_subject'),
    url(r'^delete_comment/(?P<pk>\d+)/$', comments_views.delete_comment, name='delete_comment'),
    url(r'^new_board/$',boards_views.new_board, name='new_board'),

    # user profiles
    url(r'^u/$', users_views.UsersPageView.as_view(), name='view_all_users'),
    url(r'^u/following/$', users_views.FollowingPageView.as_view(), name='view_following'),
    url(r'^u/followers/$', users_views.FollowersPageView.as_view(), name='view_all_followers'),
    url(r'^u/(?P<username>[\w.@+-]+)/$', users_views.UserProfilePageView.as_view(), name='user_profile'),
    url(r'^u/follow_user/(?P<user_id>\d+)/$',
        users_views.follow_user,
        name='follow_user'),
    url(r'^u/send_message_request/(?P<user_id>\d+)/$',
        users_views.send_message_request,
        name='send_message_request'),
    url(r'^u/accept_message_request/(?P<user_id>\d+)/$',
        users_views.accept_message_request,
        name='accept_message_request'),
    url(r'^u/block_spammer/(?P<user_id>\d+)/$',
        users_views.block_spammer,
        name='block_spammer'),
    url(r'^u/friends/all/$', users_views.all_friends, name='all_friends'),
    url(r'^u/friends/requests/$', users_views.all_message_requests, name='all_message_requests'),
    url(r'^activities/$', notifications_views.ActivitiesPageView.as_view(), name='activities'),
    url(r'^activities/check/$', notifications_views.check_activities, name='check_activities'),

    # login/logout urls
    url(r'^login/$',
        users_views.user_login,
        name='login'),
    url(r'^logout/$',
        users_views.user_logout,
        name='logout'),
    url(r'^logout-then-login/$',
        'django.contrib.auth.views.logout_then_login',
        name='logout_then_login'),

    # password change urls
    url(r'^password_change/$',
        'django.contrib.auth.views.password_change',
        name='password_change'),
    url(r'^password-change/done/$',
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'),

    # password reset
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # user registration
    url(r'^signup/$',
        users_views.register_user,
        name='signup'),

    # verify username availability in database via ajax request
    url(r'^signup/check_username/$', users_views.check_username, name='check_username'),

    # profile edit
    url(r'^profile_edit/$', users_views.profile_edit,
        name='profile_edit'),
    url(r'^picture_change/$', users_views.change_picture,
        name='picture_change'),

    # search
    url(r'^search/$',search_views.search, name='search'),
    url(r'^board_search/(?P<board_slug>[-\w]+)/$',search_views.search, name='board_search'),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^feedback/', include('feedback_form.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about-us/$', TemplateView.as_view(template_name='about_us.html'), name='about_us'),
    url(r'^legal/$', TemplateView.as_view(template_name='terms_of_service.html'), name='legal'),
    url(r'^legal/terms-of-service/$', TemplateView.as_view(template_name='terms_of_service.html'), name='terms_of_service'),
    url(r'^legal/privacy-policy/$', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),

    # report
    url(r'^banned_users/(?P<board>[-\w]+)/$',
        boards_views.banned_users,
        name='banned_users'),
    url(r'^report_subject/(?P<subject>[-\w]+)/$',
        reports_views.report_subject,
        name='report_subject'),
    url(r'^report_comment/(?P<pk>\d+)/$',
        reports_views.report_comment,
        name='report_comment'),
    url(r'^show_reports/(?P<board>[-\w]+)/$',
        reports_views.show_reports,
        name='show_reports'),
    url(r'^deactivate_subject/(?P<subject>[-\w]+)/$',
        subjects_views.deactivate_subject,
        name='deactivate_subject'),
    url(r'^deactivate_comment/(?P<pk>\d+)/$',
        comments_views.deactivate_comment,
        name='deactivate_comment'),
    url(r'^messages/', include('messenger.urls')),

    # api urls
    url(r'^api/auth/token/obtain/', obtain_jwt_token),
    url(r'^api/auth/token/refresh/', refresh_jwt_token),
    url(r'^api/auth/token/verify/', verify_jwt_token),
    url(r'^api/frontboard/', include('subjects.api.urls')),
    url(r'^api/frontboard/', include('boards.api.urls')),
    url(r'^api/frontboard/', include('reports.api.urls')),
    url(r'^api/frontboard/', include('comments.api.urls')),
    url(r'^api/users/', include('users.api.urls', namespace='users-api')),
    url(r'^api/users/', include('notifications.api.urls')),
    url(r'^api/messages/', include('messenger.api.urls', namespace='messages-api')),
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
