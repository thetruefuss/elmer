from django.conf.urls import url

from .views import NotificationListAPIView

urlpatterns = [
    url(r'^notifications/$', NotificationListAPIView.as_view(), name='list_notifications'),
]
