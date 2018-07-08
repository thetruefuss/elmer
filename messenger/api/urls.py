from django.conf.urls import url

from .views import (ContactsListAPIView, MessageCreateAPIView,
                    MessageListAPIView)

urlpatterns = [
    url(r'^contacts/$', ContactsListAPIView.as_view(), name='api_contacts'),
    url(r'^chat/$', MessageListAPIView.as_view(), name='api_chat'),
    url(r'^send/$', MessageCreateAPIView.as_view(), name='api_send'),
]
