from django.conf.urls import url

from .views import UserCreateAPIView, UserLoginAPIView, current_user

urlpatterns = [
    url(r'^login/', UserLoginAPIView.as_view(), name='users_login'),
    url(r'^signup/', UserCreateAPIView.as_view(), name='users_signup'),
    url(r'^current_user/', current_user, name='current_user'),
]
