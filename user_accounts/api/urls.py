from django.conf.urls import url

from .views import UserCreateAPIView, UserLoginAPIView

urlpatterns = [
    url(r'^login/', UserLoginAPIView.as_view(), name='users_login'),
    url(r'^signup/', UserCreateAPIView.as_view(), name='users_signup'),
]
