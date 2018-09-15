from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

import frontboard.views as frontboard_views
import user_accounts.views as useraccounts_views
from frontboard.sitemaps import SubjectSitemap
from rest_framework_jwt.views import (obtain_jwt_token, refresh_jwt_token,
                                      verify_jwt_token)

sitemaps = {
    'subjects': SubjectSitemap,
}

urlpatterns = [
    url(r'^$',frontboard_views.HomePageView.as_view(), name='home'),
    url(r'^trending/$',frontboard_views.TrendingPageView.as_view(), name='trending'),
    url(r'^s/(?P<board>[-\w]+)/(?P<subject>[-\w]+)/$',
        frontboard_views.subject_detail,
        name='subject_detail'),
    url(r'^b/$',frontboard_views.BoardsPageView.as_view(), name='view_all_boards'),
    url(r'^b/(?P<board>[-\w]+)/$',
        frontboard_views.BoardPageView.as_view(),
        name='board'),
    url(r'^b/ban_user/(?P<board>[-\w]+)/(?P<user_id>\d+)/$',
        frontboard_views.ban_user,
        name='ban_user'),
    url(r'^b/(?P<board>[-\w]+)/edit_board_cover/$',
        frontboard_views.edit_board_cover,
        name='edit_board_cover'),
    url(r'^b/(?P<board>[-\w]+)/subscription/$',
        frontboard_views.subscribe,
        name='subscribe'),
    url(r'^b/(?P<subject>[-\w]+)/like/$',
        frontboard_views.like_subject,
        name='like'),
    url(r'^load_new_comments/$', frontboard_views.load_new_comments, name='load_new_comments'),

    url(r'^u/(?P<username>[\w.@+-]+)/subscriptions/$', frontboard_views.UserSubscriptionListView.as_view(),
        name='user_subscription_list'),
    url(r'^u/(?P<username>[\w.@+-]+)/boards/$', frontboard_views.UserCreatedBoardsPageView.as_view(),
        name='user_created_boards'),
    url(r'^new_post/$',frontboard_views.new_subject, name='new_subject'),
    url(r'^delete_post/(?P<subject>[-\w]+)/$',frontboard_views.delete_subject, name='delete_subject'),
    url(r'^edit_subject/(?P<subject>[-\w]+)/$', frontboard_views.edit_subject, name='edit_subject'),
    url(r'^delete_comment/(?P<pk>\d+)/$', frontboard_views.delete_comment, name='delete_comment'),
    url(r'^new_board/$',frontboard_views.new_board, name='new_board'),

    # user profiles
    url(r'^u/$',useraccounts_views.view_all_users, name='view_all_users'),
    url(r'^u/following/$',useraccounts_views.view_following,name='view_following'),
    url(r'^u/followers/$',useraccounts_views.view_all_followers,name='view_all_followers'),
    url(r'^u/(?P<username>[\w.@+-]+)/$', useraccounts_views.user_profile, name='user_profile'),
    url(r'^u/follow_user/(?P<user_id>\d+)/$',
        useraccounts_views.follow_user,
        name='follow_user'),
    url(r'^u/send_message_request/(?P<user_id>\d+)/$',
        useraccounts_views.send_message_request,
        name='send_message_request'),
    url(r'^u/accept_message_request/(?P<user_id>\d+)/$',
        useraccounts_views.accept_message_request,
        name='accept_message_request'),
    url(r'^u/block_spammer/(?P<user_id>\d+)/$',
        useraccounts_views.block_spammer,
        name='block_spammer'),
    url(r'^u/friends/all/$', useraccounts_views.all_friends, name='all_friends'),
    url(r'^u/friends/requests/$', useraccounts_views.all_message_requests, name='all_message_requests'),
    url(r'^activities/$', useraccounts_views.activities, name='activities'),
    url(r'^activities/check/$', useraccounts_views.check_activities, name='check_activities'),

    # login/logout urls
    url(r'^login/$',
        useraccounts_views.user_login,
        name='login'),
    url(r'^logout/$',
        useraccounts_views.user_logout,
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
        useraccounts_views.register_user,
        name='signup'),

    # verify username availability in database via ajax request
    url(r'^signup/check_username/$', useraccounts_views.check_username, name='check_username'),

    # profile edit
    url(r'^profile_edit/$', useraccounts_views.profile_edit,
        name='profile_edit'),
    url(r'^picture_change/$', useraccounts_views.change_picture,
        name='picture_change'),

    # search
    url(r'^search/$',frontboard_views.search, name='search'),
    url(r'^board_search/(?P<board_slug>[-\w]+)/$',frontboard_views.search, name='board_search'),

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
        frontboard_views.banned_users,
        name='banned_users'),
    url(r'^report_subject/(?P<subject>[-\w]+)/$',
        frontboard_views.report_subject,
        name='report_subject'),
    url(r'^report_comment/(?P<pk>\d+)/$',
        frontboard_views.report_comment,
        name='report_comment'),
    url(r'^show_reports/(?P<board>[-\w]+)/$',
        frontboard_views.show_reports,
        name='show_reports'),
    url(r'^deactivate_subject/(?P<subject>[-\w]+)/$',
        frontboard_views.deactivate_subject,
        name='deactivate_subject'),
    url(r'^deactivate_comment/(?P<pk>\d+)/$',
        frontboard_views.deactivate_comment,
        name='deactivate_comment'),
    url(r'^messages/', include('messenger.urls')),

    # api urls
    url(r'^api/auth/token/obtain/', obtain_jwt_token),
    url(r'^api/auth/token/refresh/', refresh_jwt_token),
    url(r'^api/auth/token/verify/', verify_jwt_token),
    url(r'^api/frontboard/', include('frontboard.api.urls', namespace='frontboard-api')),
    url(r'^api/users/', include('user_accounts.api.urls', namespace='users-api')),
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
