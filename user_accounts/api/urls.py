from django.conf.urls import url

from .views import (NotificationListAPIView, ProfileRetrieveAPIView,
                    UserLoginAPIView, UserSignUpAPIView, current_user)

urlpatterns = [
    url(r'^login/', UserLoginAPIView.as_view(), name='users_login'),
    url(r'^signup/', UserSignUpAPIView.as_view(), name='users_signup'),
    url(r'^current_user/', current_user, name='current_user'),
    url(r'^profile/(?P<username>[-\w]+)/', ProfileRetrieveAPIView.as_view(), name='profile_info'),

    url(r'^notifications/$', NotificationListAPIView.as_view(), name='list_notifications'),
]
